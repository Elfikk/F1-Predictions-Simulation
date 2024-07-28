from RaceWeekend import RaceWeekend
from Grid import Grid
from RaceHyperparams import RaceHyperparams

class Season():

    def __init__(self, n_races) -> None:
        self.grid = Grid()
        self.hypers = RaceHyperparams()

        self.races = {i: RaceWeekend(i, self.grid, self.hypers)\
                      for i in range(1, n_races + 1)}
        
    def get_results(self, race):
        return self.races[race].get_results()

    def get_driver_names(self):
        return self.grid.get_driver_names()
    
    def get_team_names(self):
        return self.grid.get_team_names()
    
    def get_driver_to_team(self):
        return self.grid.get_driver_to_team()
        

if __name__ == "__main__":
    
    my_season = Season(24)

    print(my_season.races)