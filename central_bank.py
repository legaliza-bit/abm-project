import mesa


class CentralBank(mesa.Agent):
    """The Central Bank of the economy."""
    def __init__(self,
                 unique_id,
                 model,
                 r_base,
                 intensity,
                 inf_target
                 ):
        super().__init__(unique_id, model)
        self.r_base = r_base
        self.intensity = intensity
        self.inf_target = inf_target
        self.rate = self.set_rate()

    def set_rate(self):
        """Central Bank sets rate based on
        augmented Taylor rule.
        """
        self.rate = self.r_base + self.intensity * (
            self.model.inf_ema - self.inf_target
            )

    def step(self):
        self.set_rate()
        print(f'I set a rate {self.rate}')
