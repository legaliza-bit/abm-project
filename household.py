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
        self.productivity = np.random.uniform(1, self.sigma)
        self.wealth = np.random.normal(
            hh_params['mean_w'], hh_params['sigma_w']
            )
        self.income = 0
        self.desired_cons = np.random.normal(self.mu_k, self.sigma_k)
        self.investment = hh_params['inv_cost']
        self.demand = self.desired_cons

    def update_ptc(self):
        self.ptc *= self.sens * (self.model.inf_expec - self.bank.r_dep)

    def plan_consumption(self):
        self.desired_cons = self.ptc * self.income + np.random.normal(
            self.mu_k, self.sigma_k
            )

    def credit_operations(self):
        credit_demand = self.desired_cons + self.investment - self.wealth
        if credit_demand <= 0:  # hh is a saver
            return self.bank.store(credit_demand)
        else:
            if credit_demand > self.bank.ltv * self.wealth:
                credit_demand -= self.investment
                self.investment = 0
                if credit_demand > self.bank.ltv * self.wealth:
                    return self.bank.ltv * self.wealth
            return self.bank.lend(credit_demand)

    def invest(self):
        if self.investment != 0:
            self.productivity *= 1 + np.random.normal(self.mu_1, self.sigma)
        else:
            self.productivity *= 1 + np.random.normal(self.mu_2, self.sigma)

    def get_paid(self):
        if self in self.model.unemployed:
            self.income = 0
        else:
            self.income = self.firm.wages[self]

    def consume(self, credit):
        if credit <= 0:
            self.demand = self.desired_cons
        else:
            self.demand = credit - self.investment

    def update_wealth(self, given_credit):
        self.wealth += given_credit - self.desired_cons - self.investment

    def step(self):
        self.plan_consumption()
        credit = self.credit_operations()
        self.invest()
        self.get_paid()
        self.consume(credit)
        self.update_wealth(credit)
