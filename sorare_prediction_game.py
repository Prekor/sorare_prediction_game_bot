from manager import Manager
from game_week import GameWeek
from game_week_prediction import GameWeekPrediction


class SorarePredictionGame:
    def __init__(self, game_week: GameWeek):
        self.predictions: dict[Manager, GameWeekPrediction] = {}
        self.game_week: GameWeek = game_week

    def add_prediction(self, prediction: GameWeekPrediction):
        self.predictions[prediction.manager] = prediction

    def get_winner(self) -> Manager:
        predictions_list = list(self.predictions.values())
        assert(len(predictions_list) != 0)
        predictions_list.sort()
        return predictions_list[0].manager
