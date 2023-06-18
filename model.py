import mesa
import yaml

from household import Household
from central_bank import CentralBank
from bank import Bank
from firm import Firm

from reporters import *


with open("params.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

config_m = config['model']


class EconomyModel(mesa.Model):
    """An economy model with heterogeneous agents."""
    def __init__(self,
                 N=config_m['num_agents'],
                 r_base=config_m['r_base'],
                 intensity=config_m['intensity'],
                 inf_target=config_m['inf_target'],
                 ema_param=config_m['ema_param'],
                 trust=config_m['trust'],
                 width=config_m['width'],
                 height=config_m['height']
                 ):
        self.num_agents = N
        self.households = []
        self.inf_target = inf_target
        self.inf_actual = 0
        self.inf_ema = 0
        self.inf_expec = 0
        self.unemployed = set()
        self.unemployment = 0
        self.agg_demand = 0
        self.ema_param = ema_param
        self.trust = trust
        self.width = width
        self.height = height
        self.grid = mesa.space.MultiGrid(self.width, self.height, True)
        self.schedule = mesa.time.StagedActivation(self)
        # Create agents
        cb = CentralBank(unique_id=0,
                         model=self,
                         r_base=r_base,
                         intensity=intensity,
                         inf_target=inf_target
                         )
        self.schedule.add(cb)

        bank = Bank(unique_id=1,
                    model=self,
                    central_bank=cb,
                    bank_params=config['bank'])
        self.schedule.add(bank)

        firm = Firm(unique_id=2,
                    model=self,
                    central_bank=cb,
                    firm_params=config['firm'])
        self.schedule.add(firm)
        self.firm = firm

        for i in range(3, self.num_agents+3):
            a = Household(i,
                          self,
                          bank=bank,
                          firm=firm,
                          hh_params=config['household'])
            self.schedule.add(a)
            self.households.append(a)
            self.unemployed.add(a)

            x = (a.unique_id - 2) % self.grid.width
            y = (a.unique_id - 2) // self.grid.height
            self.grid.place_agent(a, (x, y))

        self.agg_demand = sum([a.demand for a in self.households])
        firm.output = self.agg_demand
        firm._init_employment()

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Gini": compute_gini,
                "Actual Inflation": show_inf_actual,
                "Inflation EMA": show_inf_ema,
                "Inflation Expectations": show_inf_expec,
                "Output": show_output,
                "Demand": show_demand,
                "Price": show_price
                },
            agent_reporters={
                "Wealth":
                lambda a: a.wealth if a.__class__ == Household else None,
                "Productivity":
                lambda a: a.productivity if a.__class__ == Household else None,
                "Income":
                lambda a: a.income if a.__class__ == Household else None,
                "Desired Cons":
                lambda a: a.desired_cons if a.__class__ == Household else None
                }
        )

    def upd_unemployment(self):
        self.unemployment = len(self.unemployed) / self.num_agents
        print(f'unemployment: {self.unemployment}')

    def upd_inflation(self):
        # inflation expectations are formed adaptively
        self.inf_expec = self.trust * self.inf_target + (
            1 - self.trust) * self.inf_ema

        self.inf_actual = (
            self.firm.price - self.firm.prev_price
            ) / self.firm.prev_price

        self.inf_ema = self.ema_param * self.inf_actual + (
            1 - self.ema_param) * self.inf_ema

        print(f'inflation {self.inf_actual}, inf_ema {self.inf_ema}')

    def upd_demand(self):
        self.agg_demand = sum([a.desired_cons for a in self.households])

    def step(self):
        """Advance the model by one step."""
        self.upd_unemployment()
        self.upd_inflation()
        self.upd_demand()
        print(f'agg_demand: {self.agg_demand}, output: {self.firm.output}')
        self.datacollector.collect(self)
        self.schedule.step()
