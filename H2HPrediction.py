from Grid import Grid

class H2HPrediction():

    def __init__(self, race = True) -> None:
        self.grid = Grid()

        # if race:
        self.lookup_index = 0 if race else 1

        # driver_names = self.grid.get_driver_names()
        team_names = self.grid.get_team_names()

        team_to_drivers = {team_name: [] for team_name in team_names}
        self.h2h = {}
        self.scores = {}
        driver_team_pairings = self.grid.get_driver_to_team()
        for name, team in driver_team_pairings:
            team_to_drivers[team].append(name)
            self.h2h[name] = 0
            self.scores[name] = 0

        self.driver_pairs = {}
        for team in team_to_drivers:
            name1, name2 = team_to_drivers[team]
            self.driver_pairs[name1] = name2
            self.driver_pairs[name2] = name1

        # For printing purposes
        self.team_to_drivers = team_to_drivers

    def update(self, driver_results, team_results):

        #Update counts
        for driver_name in driver_results:
            teammate_name = self.driver_pairs[driver_name]
            driver_pos = driver_results[driver_name][self.lookup_index]
            teammate_pos = driver_results[teammate_name][self.lookup_index]

            if driver_pos < teammate_pos:
                self.h2h[driver_name] += 1

        for driver_name in self.h2h:
            teammate_name = self.driver_pairs[driver_name]
            self_count, team_count = self.h2h[driver_name], self.h2h[teammate_name]
            if self_count > team_count:
                self.scores[driver_name] = 5
            else:
                self.scores[driver_name] = 0

    def __str__(self):
        state = ""
        for team in self.team_to_drivers:
            name1, name2 = self.team_to_drivers[team]
            state = state + "{:>15} {:>18} {:>18} {:>2} {:>2} {} {} \n".format(
                team, name1, name2, self.h2h[name1], self.h2h[name2], 
                self.scores[name1], self.scores[name2]
            )

        return state
    
    def score(self, player_preds):
        # H2H Scoring
        # A correct pick of the driver ahead in the H2H is worth 5pts.
        # Draws don't score.

        score = 0
        for name in player_preds:
            score += self.scores[name]
        return score


def h2h_predictions_instances():
    RaceH2H = H2HPrediction()
    QualiH2H = H2HPrediction(False)

    return [RaceH2H, QualiH2H]