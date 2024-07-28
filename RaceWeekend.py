from Grid import Grid
import numpy as np
from RaceHyperparams import RaceHyperparams
from commonFuncs import pos_sort_key

class RaceWeekend():

    def __init__(self, round_num, grid, race_hypers) -> None:

        drivers = grid.drivers
        teams = grid.teams

        #1. Generate Quali Position.

        # Generates sample of distributions for each driver, then sorts
        # the list in place according to samples. List order used to
        # generate a dictionary with position values and name keys.
        quali_order = sorted([(driver.name, np.random.normal(driver.quali_mu,\
                                                            driver.quali_std))\
                             for driver in drivers], key=pos_sort_key)
        self.quali_order = {quali_order[i][0]: i+1 for i in range(len(quali_order))}

        #2. Generate Race Position List.

        # Generates sample of distributions for each driver, then sorts
        # the list in place according to samples for race order. Final order
        # generated only after DNFs are considered.
        race_order = sorted([(driver.name, np.random.normal(driver.race_mu,\
                                                             driver.race_std))\
                             for driver in drivers], key=pos_sort_key)

        # print(race_order)

        #3. Generate Driver DNFs

        self.dnfd_drivers = set()
        dnf_laps = []

        max_lap = race_hypers.get_max_lap(round_num)
        for driver in drivers:
            p_dnf = driver.p_dnf
            uniform_sample = np.random.random_sample()
            if uniform_sample < p_dnf:
                
                # DNFs can only happen until N - 2 laps (random sample does
                # not include 1 and int always rounds down).
                dnf_lap = int(np.random.random_sample() * (max_lap-1))
                dnf_laps.append((driver.name, dnf_lap))
                self.dnfd_drivers.add(driver.name)

        #Sorted by number of laps
        dnf_laps.sort(key = pos_sort_key, reverse = True)
        race_order = [race_order[i] for i in range(len(race_order)) \
                      if race_order[i][0] not in self.dnfd_drivers] + dnf_laps

        # 4. Now have a race order.
        self.race_order = {race_order[i][0]: i+1 for i in range(len(race_order))}

        # 5. Generate the number of laps everyone has completed.
        critical_pos = np.random.normal(race_hypers.lap_mu, race_hypers.lap_std)
        critical_pos = max(2, min(int(critical_pos), 21))

        self.laps_completed = {}
        for i in range(len(race_order) - len(self.dnfd_drivers)):
            if i + 1 < critical_pos:
                self.laps_completed[race_order[i][0]] = max_lap
            else:
                self.laps_completed[race_order[i][0]] = max_lap - 1
        for driver_name, laps in dnf_laps:
            self.laps_completed[driver_name] = laps

        # for driver in self.race_order:
        #     print(self.race_order[driver], driver, self.laps_completed[driver])

        # 6. Pick FL Recipient
        self.FL = "Someone"
        uniform_sample = np.random.random_sample()
        running_p = 0
        i = 0

        while running_p < uniform_sample and i < len(race_order) - 1:
            driver_name, info = race_order[i]

            # print(driver_name)
            driver = grid.get_driver(driver_name)
            fl_prob = driver.p_fl
            running_p += fl_prob
            # print(running_p)

            i += 1

        self.FL = driver_name

        # 7. Generate number of pit stops for each driverrr.
        self.pit_stop_counts = {}

        for driver_name, info in race_order:
            driver = grid.get_driver(driver_name)
            ps_ave = driver.pit_stop_mu - 1
            ps_sample = 1 + np.random.poisson(ps_ave)

            if driver_name in self.dnfd_drivers:
                ps_sample = round(ps_sample * (self.laps_completed[driver_name] / max_lap))
            self.pit_stop_counts[driver_name] = ps_sample

        # for driver in self.race_order:
        #     print(self.race_order[driver], self.quali_order[driver], driver, self.laps_completed[driver], self.pit_stop_counts[driver])

        # 8. Generate pit stop times.

        self.min_stops = {teams[i].team: 100 for i in range(len(teams))}

        for driver_name in self.pit_stop_counts:
            if self.pit_stop_counts[driver_name]:
                driver = grid.get_driver(driver_name)
                driver_team = driver.team
                team = grid.get_team(driver_team)

                ps_mu = team.pit_time_mu

                p_min = min(np.random.exponential(ps_mu, self.pit_stop_counts[driver_name]))
                self.min_stops[team.team] = min(p_min, self.min_stops[team.team])

        # print(self.min_stops)

        # 9. Generate number of components used.

        self.eng_comps = {}
        for team in teams:
            comp_mu = team.comp_mu
            new_comps = np.random.poisson(comp_mu)
            self.eng_comps[team.team] = new_comps

        # print(self.eng_comps)

        self.repackage()

    def repackage(self):
        # Just get this into a neater format.

        self.driver_results = {}
        self.team_results = {}

        # Result format
        # Key : List
        # Key - Driver Name
        # List contents by index:
        # 0 - Race Position
        # 1 - Quali Position
        # 2 - Pit Stop Count
        # 3 - FL?
        # 4 - DNF?
        # 5 - Lap Count
        for driver_name in self.race_order:
            result = [self.race_order[driver_name], self.quali_order[driver_name],
                      self.pit_stop_counts[driver_name], False, False,
                      self.laps_completed[driver_name]]
            self.driver_results[driver_name] = result
        
        self.driver_results[self.FL][3] = True

        for driver_name in self.dnfd_drivers:
            self.driver_results[driver_name][4] = True

        # Team Result Format
        # Key : List
        # Key - Team Name
        # List Contents by Index
        # 0 - Fastest Pit Stop of the Weekend.
        # 1 - Number of new engine components taken.
        for team_name in self.min_stops:
            result = [self.min_stops[team_name], self.eng_comps[team_name]]
            self.team_results[team_name] = result

    def get_results(self):
        return self.driver_results, self.team_results


if __name__ == "__main__":

    grid = Grid()
    race_hyperparams = RaceHyperparams()

    race = RaceWeekend(14, grid, race_hyperparams)

    # print(race.quali_order)
    # print(race.race_order)

    # print(race.team_results)
    # print(race.driver_results)

    for key, value in race.team_results.items():
        print(f"{key}: {value}")

    print("")

    for key, value in race.driver_results.items():
        print(f"{key}: {value}")
