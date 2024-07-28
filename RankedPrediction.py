from RankScoring import F1ScoringMap
from Grid import Grid
from scipy.stats import rankdata

class RankedPrediction():

    def __init__(self, update_func, desc = True, driver_based = True) -> None:
    
        self.mapper = F1ScoringMap()
        self.grid = Grid()

        self.update_func = update_func
        self.desc = desc
        if driver_based:
            self.initiate_driver_counts()
        else:
            self.initiate_team_counts()

    def initiate_driver_counts(self):
        self.counts = {driver_name: 0 for driver_name in \
                       self.grid.get_driver_names()}
        self.ranks = {driver_name: 10.5 for driver_name in \
                      self.grid.get_driver_names()}

    def initiate_team_counts(self):
        self.counts = {team_name: 0 for team_name in \
                       self.grid.get_team_names()}
        self.ranks = {team_name: 5.5 for team_name in \
                      self.grid.get_team_names()}

    def update(self, driver_results, team_results):

        self.update_func(self.counts, driver_results, team_results)
        keys = [key for key in self.counts]
        data = [self.counts[key] for key in self.counts]
        ranks = rank_func(data, self.desc)

        self.ranks = {keys[i]: ranks[i] for i in range(len(keys))}

    def __str__(self):
        state = ""
        for name in self.counts:
            state = state + "{:>5} {:>20} {:>5} \n".format(self.ranks[name],
                                                     name,
                                                    self.counts[name])
                                                    
        return state

    def score(self, player_pred):
        player_rank = self.ranks[player_pred]
        score = self.mapper.map(player_rank)
        return score

class ScorelessPrediction():

    def __init__(self) -> None:
        self.mapper = F1ScoringMap()
        self.grid = Grid()

        self.round_num = 0

        self.counts = {driver_name: 0 for driver_name in \
                       self.grid.get_driver_names()}
        self.scoring_counts = {driver_name: 0 for driver_name in \
                       self.grid.get_driver_names()}
        self.ranks = {driver_name: 10.5 for driver_name in\
                       self.grid.get_driver_names()}
        
    def update(self, driver_results, team_results):

        for driver in self.counts:
            driver_count = self.counts[driver]
            if driver_count == self.round_num:
                driver_result = driver_results[driver]
                if driver_result[0] > 10:
                    self.counts[driver] += 1
                else:
                    self.scoring_counts[driver] = driver_count + 1

        self.round_num += 1

        keys = [key for key in self.scoring_counts]
        data = [self.scoring_counts[key] for key in self.scoring_counts]
        ranks = rank_func(data, False)

        self.ranks = {keys[i]: ranks[i] for i in range(len(keys))}

    def __str__(self):
        state = ""
        for name in self.counts:
            state = state + "{:>5} {:>20} {:>5} \n".format(self.ranks[name],
                                                     name,
                                                    self.scoring_counts[name])
        return state
    
    def score(self, player_pred):
        player_rank = self.ranks[player_pred]
        score = self.mapper.map(player_rank)
        return score

# The ranking function.
def rank_func(data, desc = True):
    if desc:
        return rankdata(data)
    temp = [-x for x in data]
    return rankdata(temp)

# Different update functions for different questions, updating the counts.
# Driver based ones.

def dnf_update(counts, driver_results, team_results):
    for name in counts:
        driver_result = driver_results[name]
        if driver_result[4]:
            counts[name] += 1

def laps_update(counts, driver_results, team_results):
    for name in counts:
        driver_result = driver_results[name]
        counts[name] += driver_result[5]

def pos_improv_update(counts, driver_results, team_results):
    for name in counts:
        driver_result = driver_results[name]
        race_pos, quali_pos = driver_result[0], driver_result[1]
        counts[name] += (quali_pos - race_pos)

def pit_count_update(counts, driver_results, team_results):
    for name in counts:
        driver_result = driver_results[name]
        counts[name] += driver_result[2]

def point_update(counts, driver_results, team_results):
    score_map = F1ScoringMap()
    for name in counts:
        driver_result = driver_results[name]
        race_pos = driver_result[0]
        counts[name] += score_map.map(race_pos)

# Team Based update functions

def pit_time_update(counts, driver_results, team_results):
    # print(counts)
    for team_name in counts:
        team_result = team_results[team_name]
        counts[team_name] = min(team_result[0], counts[team_name])

def engine_update(counts, driver_results, team_results):
    for team_name in counts:
        team_result = team_results[team_name]
        counts[team_name] += team_result[1]

def quali_ave_update(counts, driver_results, team_results):
    grid = Grid()

    for driver_name in driver_results:
        team = grid.get_driver(driver_name).team
        driver_result = driver_results[driver_name]
        quali_pos = driver_result[1]
        counts[team] += quali_pos

def ranked_pred_instances():

    MaxDNFs = RankedPrediction(dnf_update, False, True)
    MinLaps = RankedPrediction(laps_update, True, True)
    PositionImprover = RankedPrediction(pos_improv_update, False, True)

    ChampImprover = RankedPrediction(point_update, False, True)
    
    grid = Grid()
    # print(grid.get_driver("Max Verstappen").points2023)
    ChampImprover.counts = {driver: -grid.get_driver(driver).points2023 for \
                            driver in ChampImprover.counts}
    
    MaxPitStops = RankedPrediction(pit_count_update, False, True)
    SlowStarter = ScorelessPrediction()

    EngineComponents = RankedPrediction(engine_update, False, False)
    FastestPitStop = RankedPrediction(pit_time_update, True, False)

    FastestPitStop.counts = {team: 100 for team in FastestPitStop.counts}

    QualiAverageTeam = RankedPrediction(quali_ave_update, True, False)

    return [MaxDNFs, MinLaps, PositionImprover, ChampImprover, MaxPitStops, \
            SlowStarter, EngineComponents, FastestPitStop, QualiAverageTeam]


if __name__ == "__main__":

    MaxDNFs, MinLaps, PositionImprover, ChampImprover, MaxPitStops, \
    SlowStarter, EngineComponents, FastestPitStop, QualiAverageTeam = ranked_pred_instances()

    print(EngineComponents)