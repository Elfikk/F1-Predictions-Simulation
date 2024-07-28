class Driver():
    # Fancy schmancy class for holding driver details/parameters.

    def __init__(self) -> None:
        
        #Driver Detail
        self.name = ""
        self.team = ""

        #Qualifying Results
        self.quali_mu = 0
        self.quali_std = 0

        #Race Results
        self.race_mu = 0
        self.race_std = 0

        #Probabilities
        self.p_dnf = 0
        self.p_fl = 0

        #Pit Stop Average
        self.pit_stop_mu = 0

        #Points in 2023
        self.points2023 = 0

    def __str__(self):

        return "{:>18} {:>12} {:>5.2f}±{:.2f} {:>5.2f}±{:.2f} {:.2f} {:.2f} {:.2f} {}".format(
                                               self.name, self.team, \
                                               self.quali_mu, self.quali_std,\
                                               self.race_mu, self.race_std, \
                                               self.p_dnf, self.p_fl, \
                                               self.pit_stop_mu, self.points2023)