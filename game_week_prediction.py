from __future__ import annotations
from functools import total_ordering
from datetime import datetime

from game_week import GameWeek
from game_prediction import GamePrediction
from manager import Manager


@total_ordering
class GameWeekPrediction:
    def __init__(self, prediction_time: datetime, game_predictions: list[GamePrediction], manager: Manager):
        self.game_prediction: list[GamePrediction] = game_predictions
        self.prediction_time: datetime = prediction_time
        self.manager: Manager = manager
        self.score = 0
        self.score_without_bonus = 0
        self.total_goals = 0
        self.home_goals = 0
        self.total_goals_diff = 0
        self.home_goals_diff = 0
        self.predicted_games = 0
        self.bank_games = 0

    def calculate_results(self, game_week : GameWeek):
        for prediction in self.game_prediction:
            game_prediction = prediction.get_game()
            for game in game_week.games:
                if game_prediction == game:
                    self.score, self.total_goals_diff, self.home_goals_diff = game.get_game_results(game_prediction)
                    self.score_without_bonus = self.score
                    self.total_goals += game_prediction.home_goals + game_prediction.away_goals
                    self.home_goals += game_prediction.home_goals
                    if prediction.bank:
                        self.score *= 2
                        self.bank_games += 1
                        self.predicted_games += 1

    def get_score(self) -> int:
        return self.score

    def get_total_goals_diff(self) -> int:
        """
        Returns absolute value of all games total goal difference
        """
        return abs(self.total_goals_diff)

    def get_home_goals_diff(self) -> int:
        """
        Returns absolute value of all games home goal difference
        """
        return abs(self.home_goals_diff)

    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass