import mesa
import yaml

from agents.household import Household
from agents.central_bank import CentralBank
from agents.bank import Bank
from agents.firm import Firm

from reporters import (
    compute_gini,
    show_inf_actual,
    show_inf_ema,
    show_inf_expec,
    show_output,
    show_demand,
    show_price,
    show_rate,
    show_unemployment
)


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
                 trust=config_m['trust'],
                 ema_param=config_m['ema_param'],
                 ):
        self.num_agents = N
        self.inf_target = inf_target
        self.ema_param = ema_param
        self.trust = trust

        self.inf_actual = self.inf_ema = self.inf_expec = self.inf_ema_prev = 0

        self.households = []
        self.unemployed = set()

        self.unemployment = 0

        self.schedule = mesa.time.StagedActivation(self)
        self.to_kill = []

        # Create agents
        cb = CentralBank(unique_id=0,
                         model=self,
                         r_base=r_base,
                         intensity=intensity,
                         inf_target=inf_target
                         )
        self.schedule.add(cb)
        self.cb = cb

        bank = Bank(unique_id=1,
                    model=self,
                    central_bank=cb,
                    bank_params=config['bank'])
        self.schedule.add(bank)
        self.bank = bank

        firm = Firm(unique_id=2,
                    model=self,
                    central_bank=cb,
                    output_0=self.num_agents,
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
                "Price": show_price,
                "CB Rate": show_rate,
                "Unemployment": show_unemployment
                },
            agent_reporters={
                "Wealth":
                lambda a: a.wealth if a.__class__ == Household else None,
                "Productivity":
                lambda a: a.productivity if a.__class__ == Household else None,
                "Income":
                lambda a: a.income if a.__class__ == Household else None,
                "Desired Cons":
                lambda a: a.desired_cons if a.__class__ == Household else None,
                "PTC":
                lambda a: a.ptc if a.__class__ == Household else None
                }
        )

    def upd_unemployment(self):
        self.unemployment = len(self.unemployed) / self.num_agents

    def upd_inflation(self):
        # inflation expectations are formed adaptively
        self.inf_expec = self.trust * self.inf_target + (1 - self.trust) * self.inf_actual

        self.inf_actual = (self.firm.price - self.firm.prev_price) / self.firm.prev_price

        if self.schedule.steps < 20:
            self.inf_ema = self.inf_actual
            self.inf_ema_prev += self.inf_actual
        elif self.schedule.steps == 20:
            self.inf_ema = self.inf_ema_prev / 20
        else:
            self.inf_ema = self.ema_param * self.inf_actual + (1 - self.ema_param) * self.inf_ema

    def upd_demand(self):
        self.agg_demand = sum([a.demand for a in self.households])

    def step(self):
        """Advance the model by one step."""
        self.upd_unemployment()
        self.upd_inflation()
        self.upd_demand()
        self.datacollector.collect(self)
        self.schedule.step()
