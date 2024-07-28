from Team import Team
from Driver import Driver
from constants import *
import numpy as np

class Grid():

    #Omg a singleton
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Grid, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self) -> None:
        
        self.drivers = []
        self.teams = []

        self.initiate_grid_teams()
        self.initiate_grid_drivers()

        self.driver_to_index = {self.drivers[i].name: i for\
                                 i in range(len(self.drivers))}
        self.team_to_index = {self.teams[i].team: i for\
                               i in range(len(self.teams))}

    def initiate_grid_teams(self):

        team_data_file = "ModelData/TeamData.csv"

        with open(team_data_file, "r") as file:
            for line in file:
                if line[:4] != "Team":
                    team_name, pt_ave, engine_components = line.split(",")
                    pt_ave = float(pt_ave)
                    engine_components = int(engine_components)

                    new_team = Team()

                    new_team.team = team_name
                    new_team.pit_time_mu = pt_ave
                    new_team.comp_mu = (engine_components - 8)/NUMBER_OF_RACES

                    self.teams.append(new_team)

    def initiate_grid_drivers(self):

        # driver_to_index = {}
        fl_zero_count = 0

        # Generates Driver's probabilities of fastest laps, dnfs, mean number of pit stops,
        # and the number of points they scored in the previous season.
        # Also finds their name and team name.
        with open("ModelData/DriverData.csv", "r") as file:
            for line in file:
                # print(line[:6])
                if line[3:9] != "Driver":
                    driver_name, team_name, fl_count, dnf_count, ps_count,\
                        pts_23 = line.split(",") 

                    fl_count, dnf_count, ps_count, pts_23 = int(fl_count), \
                        int(dnf_count), int(ps_count), int(pts_23)

                    new_driver = Driver()

                    new_driver.name = driver_name
                    new_driver.team = team_name

                    new_driver.p_fl = 0 if fl_count == 0 else fl_count / (NUMBER_OF_RACES + 1)
                    new_driver.pit_stop_mu = ps_count / (NUMBER_OF_RACES - dnf_count)
                    new_driver.p_dnf = (dnf_count + 1) / (NUMBER_OF_RACES + 1)

                    new_driver.points2023 = pts_23

                    if fl_count == 0:
                        fl_zero_count += 1

                    self.drivers.append(new_driver)

        for driver in self.drivers:
            if driver.p_fl == 0:
                driver.p_fl = 1 / (fl_zero_count * (NUMBER_OF_RACES + 1))


        #Generates Driver Race Distributions
        driver_race_positions = np.genfromtxt("ModelData/RacePositions.csv", \
                                              delimiter=",", skip_header=1, \
                                              usecols=tuple(range(1, NUMBER_OF_RACES + 1)))

        for i in range(len(driver_race_positions)):
            driver = driver_race_positions[i]
            self.drivers[i].race_mu = np.nanmean(driver)
            self.drivers[i].race_std = np.nanstd(driver)

        #Generates Driver Quali Distributions
        driver_quali_positions = np.genfromtxt("ModelData/QualiPositions.csv", \
                                              delimiter=",", skip_header=1, 
                                              usecols=tuple(range(1, NUMBER_OF_RACES + 1)))

        for i in range(len(driver_quali_positions)):
            driver = driver_quali_positions[i]
            self.drivers[i].quali_mu = np.nanmean(driver)
            self.drivers[i].quali_std = np.nanstd(driver)

    def get_driver(self, name):
        return self.drivers[self.driver_to_index[name]]

    def get_team(self, team):
        return self.teams[self.team_to_index[team]]
    
    def get_driver_names(self):
        return [self.drivers[i].name for i in range(len(self.drivers))]

    def get_driver_to_team(self):
        return [(self.drivers[i].name, self.drivers[i].team) for i in\
                range(len(self.drivers))]

    def get_team_names(self):
        return [self.teams[i].team for i in range(len(self.teams))]

if __name__ == "__main__":

    grid = Grid()

    print(vars(grid.drivers[5]))