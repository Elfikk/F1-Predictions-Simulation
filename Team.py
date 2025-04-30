class Team():
    # Less fancy schmancy class for holding team details. Basically a dictionary.
    # This should really be a frozen dataclass.

    def __init__(self) -> None:

        #Team Name
        self.team = ""

        # Average Pit Stop Rate and Standard Deviation
        # We are treating the speed at which stops are done as normally distributed
        # from DHL data. Really though we should have two Gaussians, one for short
        # standard pit stops, and one with something wrong i.e a front wing and a
        # probability
        self.pit_rate_mu = 0
        self.pit_rate_std = 0
        self.pit_rate_poor_mu = 0
        self.pit_rate_poor_std = 0
        self.p_poor = 0

        #Number of components used per race
        self.comp_mu = 0

    def __str__(self):
        return f"{self.team:>15} {self.comp_mu:.2f} {self.pit_rate_mu:.2f}±{self.pit_rate_std:.2f} / {self.pit_rate_poor_mu:.2f}±{self.pit_rate_poor_std:.2f} @ {self.p_poor:.2f}"