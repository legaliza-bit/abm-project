import mesa
import numpy as np


class Household(mesa.Agent):
    """Household agent."""
    def __init__(self,
                 unique_id,
                 model,
                 bank,
                 firm,
                 hh_params
                 ):
        super().__init__(unique_id, model)
        self.bank = bank
        self.firm = firm
        self.ptc = hh_params['ptc']
        self.sens = hh_params['sens']
        self.mu_k = hh_params['mu_k']
        self.sigma_k = hh_params['sigma_k']
        self.mu_1 = hh_params['mu_1']
        self.mu_2 = hh_params['mu_2']
        self.sigma = hh_params['sigma']
        self.productivity = np.random.normal(1, self.sigma)
        self.wealth = np.random.normal(
            hh_params['mean_w'], hh_params['sigma_w']
            )
        self.income = 0
        self.desired_cons = np.random.normal(self.mu_k, self.sigma_k)
        self.investment = hh_params['inv_cost']
        self.demand = self.desired_cons

    def update_ptc(self):
        """Update household's propensity to consume out of income
        based on inflation expectations and bank deposit rate.
        """
        self.ptc *= (1 + self.sens * (self.model.inf_expec - self.bank.r_dep)
                    ) * (1 + 0.01 * (self.firm.prev_price - self.firm.price))
        if self.ptc < 0:
            self.ptc = 0
        elif self.ptc > 1:
            self.ptc = 1

    def plan_consumption(self):
        """Household plans its consumption based on expected income (which is
        just income of the previous period) and adds a random component.
        """
        self.desired_cons = self.ptc * self.income + np.random.normal(
            self.mu_k, self.sigma_k)

    def get_paid(self):
        """Household receives its wage from firm if they're employed
        in the current period.
        """
        if self in self.model.unemployed:
            self.income = 0
        else:
            self.income = self.firm.wages[self]

        self.wealth += self.income

    def credit_operations(self) -> tuple[int, int]:
        """Household determines whether to save or borrow based on
        desired consumption and actual wealth, including current wage.
        Here, either the bank's lend or store method is called, which returns
        credit amount with interest that is added to household wealth
        at the end of period. Household may be credit constrained, if
        its credit demand is bigger than a fraction of its wealth. In this
        case the highest available amount is lended.
        """
        credit_demand = self.desired_cons + self.investment - self.wealth
        if credit_demand <= 0:  # hh is a saver
            return credit_demand, self.bank.store(credit_demand)
        else:
            if credit_demand > self.bank.ltv * self.wealth:
                credit_demand -= self.investment
                self.investment = 0
                if credit_demand > self.bank.ltv * self.wealth:
                    credit_demand = self.bank.ltv * self.wealth
            return credit_demand, self.bank.lend(credit_demand)

    def invest(self):
        """Household invests a fixed amount to increase its productivity.
        If household is credit constrained it may choose not to invest.
        """
        if self.investment != 0:
            self.productivity *= (1 + np.random.normal(self.mu_1, self.sigma))
        else:
            self.productivity *= (1 + np.random.normal(self.mu_2, self.sigma))

    def consume(self, given_credit: int):
        """Household spends wealth on consumption."""
        if given_credit <= 0:  # hh is a saver and can afford desired cons lvl
            self.demand = self.desired_cons
        else:  # hh is a borrower and may be credit constrained
            self.demand = min(
                self.desired_cons, self.wealth + given_credit - self.investment
                )

    def update_wealth(self, interest: int):
        self.wealth += interest - self.demand

        # if self.wealth <= 0:
        #     self.model.to_kill.append(self)
        #     self.model.households.remove(self)
        #     if self in self.model.unemployed:
        #         self.model.unemployed.remove(self)
        #     else:
        #         self.firm.wages.pop(self)

    def step(self):
        self.plan_consumption()
        self.get_paid()
        given_credit, interest = self.credit_operations()
        self.invest()
        self.consume(given_credit)
        self.update_wealth(interest)
        self.update_ptc()
