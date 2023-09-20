import mesa
from agents.household import Household
import numpy as np
from random import choice


class Firm(mesa.Agent):
    """Aggregate representative firm."""
    def __init__(
            self,
            unique_id,
            model,
            central_bank,
            output_0,
            firm_params
            ):
        super().__init__(unique_id, model)
        self.cb = central_bank
        self.output = self.model.num_agents
        self.adj_p = firm_params['adj_p']
        self.adj_w = firm_params['adj_w']
        self.nu_2 = firm_params['nu_2']
        self.nu_1 = self.nu_2
        self.sens = firm_params['sens']

        self.wages = {}

        self.prev_price = self.price = 1

    def _init_employment(self):
        """Randomly initialize employment in the model."""
        N_empl = np.random.randint(
            self.model.num_agents // 2, self.model.num_agents
            )
        empl = []
        for _ in range(N_empl):
            new_e = self.model.unemployed.pop()
            empl.append(new_e)

        self.base_wage = self.output / N_empl
        self._init_wages(empl, empl)

    def _init_wages(self,
                    curr_employees: list[Household],
                    new_employees: list[Household]
                    ) -> dict[Household, int]:
        """Initialize wages for hired employees:
        Each period we compute a baseline currently paid per
        'productivity unit' and then multiply by employee productivity
        to get their wage. Then we add the employee and their wage to dict.
        """

        for e in new_employees:
            self.wages[e] = self.base_wage * e.productivity

    def det_state(self) -> int:
        """Determine if there is excess demand or excess
        supply in the economy to adjust output, price and wages.
        """
        gap = self.output - self.model.agg_demand
        if gap <= 0:
            self.state = True  # case of excess demand
        else:
            self.state = False  # case of excess supply
        return gap

    def upd_price(self):
        # store previous price to compute inflation
        self.prev_price = self.price

        if self.state:
            self.price *= (1 + self.sens * self.model.inf_expec) * (
                1 + self.adj_p * np.random.uniform(0, 1))
        else:
            self.price *= (1 + self.sens * self.model.inf_expec) * (
                1 - self.adj_p * np.random.uniform(0, 1))

    def upd_output(self, gap):
        # update propensity to increase output and wages
        if not self.model.unemployed:
            self.nu_1 = 0
        else:
            self.nu_1 = self.cb.rate * self.nu_2

        if self.state:
            self.output = self.output - self.nu_1 * gap
        else:
            self.output = self.output - self.nu_2 * gap

    def upd_workforce(self, gap: int):
        """Hire or fire employees.
        :param gap: excess demand (if negative) or supply (if positive)

        If there is excess demand in the economy, the firm hires
        proportionally to gap. In case of excess supply it fires.
        New employees are taken randomly from the set of unemployed workers
        in the model. Employees are fired randomly also.
        """
        self.base_wage = self.output / sum([e.productivity for e in self.wages.keys()])

        if self.state:
            self.base_wage *= (1 + self.sens * (1 - self.nu_1) * (
                    1 - self.model.unemployment) * np.random.uniform(0, 1)) * (
                    1 + self.sens * self.model.inf_expec)

            for e in self.wages.keys():
                self.wages[e] = self.base_wage * e.productivity

            n_to_hire = int(self.nu_1 * -gap / self.output * len(self.wages))
            new_empl = []
            for _ in range(n_to_hire):
                if not self.model.unemployed:
                    break
                new_e = self.model.unemployed.pop()
                new_empl.append(new_e)
            self._init_wages(list(self.wages.keys()), new_empl)

        else:
            self.base_wage *= (
                    1 - self.nu_2 * self.model.unemployment * np.random.uniform(0, 1)
                    ) * (1 + self.sens * self.model.inf_expec)

            for e in self.wages.keys():
                self.wages[e] = self.base_wage * e.productivity

            n_to_fire = int(self.nu_2 * gap / self.output * len(self.wages))
            for _ in range(n_to_fire):
                fired = choice(list(self.wages))
                self.wages.pop(fired)
                self.model.unemployed.add(fired)

    def step(self):
        gap = self.det_state()
        self.upd_workforce(gap)
        self.upd_price()
        self.upd_output(gap)
