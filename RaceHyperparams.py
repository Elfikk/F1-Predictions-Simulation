import numpy as np

class RaceHyperparams():

    def __init__(self, races_file = "ModelData/RaceMetadata.csv",
                 lapping_file = "ModelData/CriticalLap.csv") -> None:
        
        # self.round_to_lap = {
        #     1: 57,
        #     2: 50,
        #     3: 58,
        #     4: 53,
        #     5: 56,
        #     6: 57,
        #     7: 63, 
        #     8: 78,
        #     9: 70,
        #     10: 66,
        #     11: 71,
        #     12: 52,
        #     13: 70,
        #     14: 44,
        #     15: 72,
        #     16: 53,
        #     17: 51,
        #     18: 62,
        #     19: 56,
        #     20: 71,
        #     21: 71,
        #     22: 50,
        #     23: 57,
        #     24: 58
        # }

        self.round_to_lap = {}
        self.name_to_round = {}
        self.round_to_name = {}

        self.load_race_metadata(races_file)
        self.lap_mu, self.lap_std = self.load_lapping_data(lapping_file)

    def load_lapping_data(self, file):

        lines = []

        with open(file, "r") as f:
            for line in f:
                # print(line)
                lines.append(line.split(",")[1])

        lines = lines[1:]
        lines = [int(laps) for laps in lines]

        mu = np.mean(lines)
        std = np.std(lines)

        return mu, std

    def load_race_metadata(self, file):

        lines = []

        with open(file, "r") as f:
            for line in f:
                # print(line)
                lines.append(line.split(","))

        lines = lines[1:]

        for line in lines:
            # print(line)
            round_num, race_name, laps = line

            round_num = int(round_num)
            laps = int(laps)

            self.round_to_lap[round_num] = laps
            self.name_to_round[race_name] = round_num
            self.round_to_name[round_num] = race_name

    def get_max_lap(self, round_num):
        if round_num in self.round_to_lap:
            return self.round_to_lap[round_num]
        return 55

if __name__ == "__main__":

    rh = RaceHyperparams()

    print(rh.lap_mu, rh.lap_std)

    laps = [rh.round_to_lap[key] for key in rh.round_to_lap]
    print(sum(laps))