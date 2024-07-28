from PredictionPlayer import PredictionPlayer
from Predictions2024 import get_all_preds_2024
from Season import Season

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

                    # print(player_name, pred_key)
                    # print()

                    pred_obj = self.preds[pred_key]
                    player_preds = player_obj.preds[pred_key]
                    score = pred_obj.score(player_preds)
                    running_score += score

                    # if i == 1:
                        # print(pred_key, score)
                
                # print(running_score)
                
                self.running_scores[player_name].append(running_score)

    def generate_stats(self, runs = 1000):

        scores_tots = {player_name: 24 * [0] for player_name in self.players}
        scores_tots_sq = {player_name: 24 * [0] for player_name in self.players}

        for i in range(runs):
            self.generate_pred_season()

            for player_name in self.running_scores:
                player_scores = self.running_scores[player_name]
                for i in range(len(player_scores)):
                    score = player_scores[i]
                    scores_tots[player_name][i] += score
                    scores_tots_sq[player_name][i] += score**2

        self.score_means = {name: [score / runs for score in scores_tots[name]] \
                            for name in scores_tots}
        score_sq_mu =  {name: [score / runs for score in scores_tots_sq[name]] \
                        for name in scores_tots}
        self.score_std = {name: \
                          [(score_sq_mu[name][i] - self.score_means[name][i]**2)**0.5 \
                           for i in range(24)] for name in scores_tots}    
    

if __name__ == "__main__":

    my_fav = PredictionStats()
    my_fav.generate_pred_season()
    # my_fav.generate_stats(10)
