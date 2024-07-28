from RankScoring import F1ScoringMap
from Season import Season
from commonFuncs import pos_sort_key
# import numpy as np
from Grid import Grid
from scipy.stats import spearmanr

class DriverChampionship():

    def __init__(self) -> None:
        
        grid = Grid()
        driver_names = grid.get_driver_names()

        self.raw_results = {driver_names[i]: [] \
                            for i in range(len(driver_names))}
        self.champ_order = [driver_names[i] for i in range(len(driver_names))]
        self.points = {driver_names[i]: 0 for i in range(len(driver_names))}

    def update(self, driver_results, team_results = []):

        #MAP EM - TODO: Make F1ScoringMap a Singleton. Will be used elsewhere.
        score_map = F1ScoringMap()

        for driver_name in driver_results:
            
            race_result = driver_results[driver_name]
            # print(driver_name, race_result)
            pos, fl = race_result[0], race_result[3]
            # print(pos, fl)

            #Sort raw results for tiebreaker purposes
            self.raw_results[driver_name] = sorted(self.raw_results[driver_name]\
                                                    + [pos])

            pts = score_map.map(pos)
            if fl and pts:
                pts += 1
                # print(driver_name, pts)

            self.points[driver_name] += pts

        self.determine_champ_order()

    def determine_champ_order(self, printPrint = False):

        # First sort by the points.
        driver_points = sorted(list(self.points.items()), key=pos_sort_key,\
                                reverse=True)
        # print(driver_points)
        self.champ_order = [driver for driver, pts in driver_points]

        L, R = 0, 1
        slices = []

        while R < len(driver_points):

            pts_l, pts_r = driver_points[L][1], driver_points[R][1]

            if printPrint:
                print(L, R, slices, pts_l, pts_r)

            if pts_l == pts_r:
                #Move right index until slice ended.
                while R < len(driver_points) and pts_l == pts_r:
                    pts_r = driver_points[R][1]
                    R += 1

                if pts_l == pts_r:
                    slices.append((L, R))
                else:
                    slices.append((L, R - 1))
                L = R-1
                # R += 1

                if printPrint:
                    print("post loop")
                    print(L, R, slices, pts_l, pts_r)
            else:
                L += 1
                R += 1

        for slice in slices:

            driver_names = [self.champ_order[i] for i in range(slice[0], slice[1])]

            if printPrint:
                print(driver_names)

            driver_names = sorted(driver_names, key = lambda x: self.raw_results[x])
            
            if printPrint:
                print(driver_names)

            for i in range(len(driver_names)):
                self.champ_order[slice[0] + i] = driver_names[i]

    def __str__(self):

        order_string = ""
        for i in range(len(self.champ_order)):
            driver = self.champ_order[i]
            driver_string = str(i + 1) + " " + driver + " " + str(self.points[driver]) + "\n"
            order_string = order_string + driver_string

        return order_string
    
    def get_champ_order(self):
        return self.champ_order
    
    def score(self, player_preds):
        a, b = [i + 1 for i in range(len(self.champ_order))], []

        for i in range(len(self.champ_order)):
            driver_name = self.champ_order[i]
            b.append(player_preds[driver_name])

        cor, p = spearmanr(a, b)

        score = int(round(400 * (cor - 0.5), 0))

        return score

class ConstructorChampionship():

    def __init__(self) -> None:
        
        grid = Grid()

        team_names = grid.get_team_names()
        driver_to_teams = grid.get_driver_to_team()

        self.raw_results = {team_names[i]: [] \
                            for i in range(len(team_names))}
        self.champ_order = [team_names[i] for i in range(len(team_names))]
        self.points = {team_names[i]: 0 for i in range(len(team_names))}
        self.driver_to_team = {driver: team for driver, team in driver_to_teams}

        self.running_order = {team_names[i]: [] for i in range(len(team_names))}

    def update(self, driver_results, team_results = []):

        #MAP EM - TODO: Make F1ScoringMap a Singleton. Will be used elsewhere.
        score_map = F1ScoringMap()

        for driver_name in driver_results:
            
            race_result = driver_results[driver_name]
            # print(driver_name, race_result)
            pos, fl = race_result[0], race_result[3]
            # print(pos, fl)
            team_name = self.driver_to_team[driver_name]

            #Sort raw results for tiebreaker purposes
            self.raw_results[team_name] = sorted(self.raw_results[team_name]\
                                                    + [pos])

            pts = score_map.map(pos)
            if fl and pts:
                pts += 1
                # print(driver_name, pts)

            self.points[team_name] += pts

        self.determine_champ_order()   

        for i in range(len(self.champ_order)):
            name = self.champ_order[i]
            self.running_order[name].append(i + 1)

    def determine_champ_order(self, printPrint = False):

        # First sort by the points.
        driver_points = sorted(list(self.points.items()), key=pos_sort_key,\
                                reverse=True)
        # print(driver_points)
        self.champ_order = [driver for driver, pts in driver_points]

        L, R = 0, 1
        slices = []

        while R < len(driver_points):

            pts_l, pts_r = driver_points[L][1], driver_points[R][1]

            if printPrint:
                print(L, R, slices, pts_l, pts_r)

            if pts_l == pts_r:
                #Move right index until slice ended.
                while R < len(driver_points) and pts_l == pts_r:
                    pts_r = driver_points[R][1]
                    R += 1

                if pts_l == pts_r:
                    slices.append((L, R))
                else:
                    slices.append((L, R - 1))
                L = R-1
                # R += 1

                if printPrint:
                    print("post loop")
                    print(L, R, slices, pts_l, pts_r)
            else:
                L += 1
                R += 1

        for slice in slices:

            driver_names = [self.champ_order[i] for i in range(slice[0], slice[1])]

            if printPrint:
                print(driver_names)

            driver_names = sorted(driver_names, key = lambda x: self.raw_results[x])
            
            if printPrint:
                print(driver_names)

            for i in range(len(driver_names)):
                self.champ_order[slice[0] + i] = driver_names[i]

    def __str__(self):

        order_string = ""
        for i in range(len(self.champ_order)):
            driver = self.champ_order[i]
            driver_string = str(i + 1) + " " + driver + " " + str(self.points[driver]) + "\n"
            order_string = order_string + driver_string

        return order_string

    def get_champ_order(self):
        return self.champ_order
    
    def score(self, player_preds):
        a, b = [i + 1 for i in range(len(self.champ_order))], []

        for i in range(len(self.champ_order)):
            team_name = self.champ_order[i]
            b.append(player_preds[team_name])

        cor, p = spearmanr(a, b)

        score = int(round(400 * (cor - 0.5), 0))

        return score

class NAfterN():

    def __init__(self):

        grid = Grid()
        driver_names = grid.get_driver_names()
        self.d_champ = DriverChampionship()

        self.N = 0

        self.running_order = {driver_names[i]: [] for i in range(len(driver_names))}
        self.scores = {driver_names[i]: [] for i in range(len(driver_names))}

    def update(self, driver_results, team_results = []):

        self.d_champ.update(driver_results, team_results)
        self.N += 1

        for i in range(len(self.d_champ.champ_order)):
            name = self.d_champ.champ_order[i]
            self.running_order[name].append(i + 1)

        score_map = F1ScoringMap()

        for driver_name in self.running_order:
            champ_pos = self.running_order[driver_name][-1]
            rank = abs(champ_pos - self.N) + 1
            self.scores[driver_name].append(score_map.map(rank))

    def __str__(self):
        state = ""
        for driver_name in self.scores:
            state = state + "{:>18} {} {} \n".format(driver_name, 
                                                     self.running_order[driver_name][:6],
                                                     self.scores[driver_name][:6])
        return state
    
    def score(self, player_preds):
        score = 0
        for round_num in player_preds:
            if self.N + 1 > round_num:
                index = round_num - 1
                driver_name = player_preds[round_num]
                score += self.scores[driver_name][index]
        return score

if __name__ == "__main__":

    test_season = Season(24)
    d_champ = DriverChampionship(test_season.get_driver_names())

    for i in range(1, 25):
        driver_results, team_results = test_season.get_results(i)
        d_champ.update(driver_results)
        # print(d_champ.champ_order[0])

    print(d_champ)