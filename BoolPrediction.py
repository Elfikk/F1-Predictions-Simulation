from Grid import Grid
from RaceWeekend import RaceWeekend
from RaceHyperparams import RaceHyperparams

class BoolPred():

    def __init__(self, cond_func, update_func) -> None:
        
        # self.counts = {}
        self.grid = Grid()

        driver_names = self.grid.get_driver_names()

        self.counts = {name: 0 for name in driver_names}
        self.bool = {name: False for name in driver_names}

        self.update_func = update_func
        self.cond_func = cond_func

    def update(self, driver_results, team_results):
        #Pass by reference in Python 
        self.update_func(self.counts, driver_results, team_results)

        #Update boolean dictionary.
        self.bool = self.cond_func(self.counts)

    def __str__(self) -> str:
        
        state = ""
        for name in self.counts:
            state = state + "{:>18} {} {} \n".format(name,
                                                    self.counts[name],
                                                    self.bool[name])
        return state

    def score(self, player_preds):
        # Boolean score rules
        # If actual state is true and predicted state is true, +5
        # If the predicted state is wrong, -3
        # If the predicted and actual states are both false, 0
        score = 0

        for name in player_preds:
            state, pred_state = self.bool[name], player_preds[name]
            if state != pred_state:
                score += -3
            else:
                if state:
                    score += 5
        return score

# Couple of condition function generators

def range_condition(min_val, max_val):
    #Integer condition only, intended for counts.
    #min val and max val are inclusive.
    range_vals = set(range(min_val, max_val + 1))

    def range_check(count_dict):
        bool_dict = {}
        for key in count_dict:
            if count_dict[key] in range_vals:
                bool_dict[key] = True
            else:
                bool_dict[key] = False
        return bool_dict

    return range_check

def geq_condition(min_val):
    #Greater or equal to count condition.

    def geq_check(count_dict):
        bool_dict = {}
        for key in count_dict:
            if count_dict[key] >= min_val:
                bool_dict[key] = True
            else:
                bool_dict[key] = False
        return bool_dict

    return geq_check

# Update functions

def podium_update(count_dict, driver_results, team_results):

    for driver_name in count_dict:
        driver_result = driver_results[driver_name]
        race_pos = driver_result[0]
        if race_pos < 4:
            count_dict[driver_name] += 1

def pole_update(count_dict, driver_results, team_results):

    for driver_name in count_dict:
        driver_result = driver_results[driver_name]
        quali_pos = driver_result[1]
        if quali_pos == 1:
            count_dict[driver_name] += 1

def fl_update(count_dict, driver_results, team_results):

    for driver_name in count_dict:
        driver_result = driver_results[driver_name]
        fl = driver_result[3]
        if fl:
            count_dict[driver_name] += 1

def q1_update(count_dict, driver_results, team_results):

    for driver_name in count_dict:
        driver_result = driver_results[driver_name]
        quali_pos = driver_result[1]
        if quali_pos > 15:
            count_dict[driver_name] += 1

def monaco_update(count_dict, driver_results, team_results):

    # Most sensible way to check this? Bodge is to check the number of laps.
    is_monaco = False

    for driver_name in count_dict:
        driver_result = driver_results[driver_name]
        race_pos, laps_max = driver_result[0], driver_result[-1]
        if race_pos == 1:
            if laps_max == 78:
                is_monaco = True

    if is_monaco:
        for driver_name in count_dict:
            driver_result = driver_results[driver_name]
            race_pos = driver_result[0]
            if race_pos < 11:
                count_dict[driver_name] += 1

# Instances of the bool predictions.

def bool_pred_instances():

    Podiums = BoolPred(geq_condition(1), podium_update)
    Poles = BoolPred(geq_condition(1), pole_update)
    FLs = BoolPred(geq_condition(1), fl_update)
    Q1s = BoolPred(geq_condition(5), q1_update)
    Monaco = BoolPred(geq_condition(1), monaco_update)

    return [Podiums, Poles, FLs, Q1s, Monaco]

if __name__ == "__main__":

   
    # Podiums = BoolPred(geq_condition(1), podium_update) 
    # print(Podiums)

    Podiums, Poles, FLs, Q1s, Monaco = bool_pred_instances()

    hypers = RaceHyperparams()
    weekend = RaceWeekend(8, Grid(), hypers)

    driver_res, team_res = weekend.get_results()

    # print(driver_res.items)
    for driver in driver_res:
        print(driver, driver_res[driver])

    Monaco.update(driver_res, team_res)

    # for i in range(5):
    #     Q1s.update(driver_res, team_res)


    print(Monaco)