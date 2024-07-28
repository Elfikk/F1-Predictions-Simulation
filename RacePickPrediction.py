from RaceHyperparams import RaceHyperparams
from RankScoring import F1ScoringMap

class RacePickPrediction():

    def __init__(self, score_func):

        self.race_hypers = RaceHyperparams()
        self.race_to_score = {race_name: 0 for race_name in \
                              self.race_hypers.name_to_round}
        self.race_num = 0

        self.score_func = score_func

    def update(self, driver_results, team_results):
        self.race_num += 1
        race_name = self.race_hypers.round_to_name[self.race_num]
        score = self.score_func(driver_results, team_results)
        self.race_to_score[race_name] = score

    def __str__(self) -> str:
        state = ""
        for race_name in self.race_to_score:
            state = state + "{:>15} {:>3} \n".format(race_name, 
                                                     self.race_to_score[race_name])
        return state
    
    def score(self, player_preds):
        score = 0
        for race in player_preds:
            score += self.race_to_score[race]
        return score

#All the scoring functions in the world.

def hulk_quali_score(driver_results, team_results):
    hulk_name = "Nico Hulkenberg"
    hulk_result = driver_results[hulk_name]
    hulk_quali_pos = hulk_result[1]

    da_map = F1ScoringMap()
    return da_map.map(hulk_quali_pos)

def gasly_race_score(driver_results, team_results):
    gasly_name = "Pierre Gasly"
    gasly_result = driver_results[gasly_name]
    gasly_race_pos = gasly_result[0]

    da_map = F1ScoringMap()
    return da_map.map(gasly_race_pos)

def blowy_engines_score(driver_results, team_results):
    dnf_count = 0
    for driver_name in driver_results:
        driver_result = driver_results[driver_name]
        dnf = driver_result[4]

        if dnf:
            dnf_count += 1

    return 5 * dnf_count

def pick_prediction_instances():

    HulkQuali = RacePickPrediction(hulk_quali_score)
    GaslyRace = RacePickPrediction(gasly_race_score)
    BlowyEngines = RacePickPrediction(blowy_engines_score)

    return [HulkQuali, GaslyRace, BlowyEngines]