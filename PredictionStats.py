from constants import PREDICTION_TYPES_2024
from PredictionPlayer import PredictionPlayer
from Predictions2024 import get_all_preds_2024
from Season import Season

from pathlib import Path
import pickle
import tqdm

class PredictionStats():

    def __init__(self) -> None:

        self.players = {}
        player_names = set(["Benedict",
                            "Carla",
                            "Damian",
                            "Jarek",
                            "Josh",
                            "Kacper",
                            "Suley"])

        for name in player_names:
            # print(name)
            file_dir = "PredictionSpreadsheets/{}.xlsx".format(name)
            self.players[name] = PredictionPlayer(file_dir)

        self.initialise_score_stats()

    def generate_pred_season(self):

        self.preds = get_all_preds_2024()
        self.season = Season(24)

        self.running_scores = {player_name: [] for player_name in self.players}

        for i in range(1, 25):
            driver_results, team_results = self.season.get_results(i)

            for pred_key in self.preds:
                pred_obj = self.preds[pred_key]
                pred_obj.update(driver_results, team_results)

            for player_name in self.players:

                running_score = 0
                player_obj = self.players[player_name]
                for pred_key in self.preds:

                    pred_obj = self.preds[pred_key]
                    player_preds = player_obj.preds[pred_key]
                    score = pred_obj.score(player_preds)
                    running_score += score

                self.running_scores[player_name].append(running_score)

    def initialise_score_stats(self):
        self.runs = 0
        self.scores_tots = {player_name: 24 * [0] for player_name in self.players}
        self.scores_tots_sq = {player_name: 24 * [0] for player_name in self.players}
        self.score_histograms = {player_name: 150 * [0] for player_name in self.players}
        self.mean_scores = {player_name: [] for player_name in self.players}
        self.point_dist = {player_name: {key: [] for key in PREDICTION_TYPES_2024} for player_name in self.players}

    def generate_stats(self, runs = 1000):
        self.runs += runs

        for i in tqdm.tqdm(range(runs)):
            self.generate_pred_season()
            for player_name in self.running_scores:
                player_scores = self.running_scores[player_name]
                for i in range(len(player_scores)):
                    score = player_scores[i]
                    self.scores_tots[player_name][i] += score
                    self.scores_tots_sq[player_name][i] += score**2

            mean_score = 0
            for player_name in self.running_scores:
                mean_score += self.running_scores[player_name][-1]
            mean_score = mean_score / len(self.running_scores)

            for player_name in self.running_scores:
                player_scores = self.running_scores[player_name]
                score = player_scores[-1]
                score_bin = score // 10
                self.score_histograms[player_name][score_bin] += 1
                self.mean_scores[player_name].append(score - mean_score)

            for player_name in self.running_scores:
                player_obj = self.players[player_name]
                for pred_type in PREDICTION_TYPES_2024:
                    type_score = 0
                    for pred_key in PREDICTION_TYPES_2024[pred_type]:
                        pred_obj = self.preds[pred_key]
                        player_preds = player_obj.preds[pred_key]
                        score = pred_obj.score(player_preds)
                        type_score += score
                    self.point_dist[player_name][pred_type].append(type_score)

        self.calculate_gauss_stats()

    def load_checkpoint(self, path: Path):
        with open(path, "rb") as file:
            unpickled_data = pickle.load(file)
        self.runs = unpickled_data[0]
        self.scores_tots = unpickled_data[1]
        self.scores_tots_sq = unpickled_data[2]
        self.score_histograms = unpickled_data[3]
        self.mean_scores = unpickled_data[4]
        self.calculate_gauss_stats()
        if len(unpickled_data) > 5:
            self.point_dist = unpickled_data[5]

    def save_checkpoint(self, path: Path):
        to_pickle = [
            self.runs,
            self.scores_tots,
            self.scores_tots_sq,
            self.score_histograms,
            self.mean_scores
        ]
        with open(path, "wb") as file:
            pickle.dump(to_pickle, file)

    def calculate_gauss_stats(self):
        self.score_means = {name: [score / self.runs for score in self.scores_tots[name]] \
                            for name in self.scores_tots}
        score_sq_mu =  {name: [score / self.runs for score in self.scores_tots_sq[name]] \
                        for name in self.scores_tots}
        self.score_std = {name: \
                          [(score_sq_mu[name][i] - self.score_means[name][i]**2)**0.5 \
                           for i in range(24)] for name in self.scores_tots}

if __name__ == "__main__":

    my_fav = PredictionStats()
    my_fav.generate_pred_season()
    # my_fav.generate_stats(10)
