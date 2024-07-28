class Team():
    # Less fancy schmancy class for holding team details. Basically a dictionary.

    def __init__(self) -> None:
        
        #Pit Stop Name
        self.team = ""

        #Average Pit Stop Duration
        self.pit_time_mu = 0
        
        #Number of components used per race
        self.comp_mu = 0

