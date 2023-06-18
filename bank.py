import mesa


class Bank(mesa.Agent):
    """Aggregate representative bank."""
    def __init__(self,
                 unique_id,
                 model,
                 central_bank,
                 bank_params):
        super().__init__(unique_id, model)
        self.cb = central_bank
        self.ltv = bank_params['ltv']
        self.mu_dep = bank_params['mu_dep']
        self.mu_loan = bank_params['mu_loan']

    def update_rates(self):
        """Bank updates rates every period based on
        previous Central Bank rate.
        """
        self.r_loan = self.cb.rate * (1 + self.mu_loan)
        self.r_dep = self.cb.rate * (1 - self.mu_dep)

    def lend(self, amount: int) -> int:
        """Method is called when household wants
        to lend money. It returns the lended amount
        with interest that is then substracted from
        household wealth at the end of period.
        """
        return - amount * (1 + self.r_loan)

    def store(self, amount: int) -> int:
        """Method is called when household wants
        to save money. It returns the saved amount
        with interest that is then added to
        household wealth at the end of period.
        """
        return - amount * (1 + self.r_dep)

    def step(self):
        self.update_rates()
