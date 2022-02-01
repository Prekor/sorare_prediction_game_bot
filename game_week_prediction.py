from __future__ import annotations
from functools import total_ordering
from datetime import datetime

from game_prediction import GamePrediction
from manager import Manager


@total_ordering
class GameWeekPrediction:
    def __init__(self, prediction_time: datetime, game_predictions: list[GamePrediction], manager: Manager):
        self.game_predictions: list[GamePrediction] = game_predictions
        self.prediction_time: datetime = prediction_time
        self.manager: Manager = manager

    def get_score(self) -> int:
        score = 0
        for game_prediction in self.game_predictions:
            score += game_prediction.get_score()
        return score

    def get_total_goals_diff(self) -> int:
        total_goals_diff = 0
        for game in self.game_predictions:
            total_goals_diff += game.get_total_goals_diff()
        return abs(total_goals_diff)

    def get_home_goals_diff(self) -> int:
        home_goals_diff = 0
        for game in self.game_predictions:
            home_goals_diff += game.get_home_goals_diff()
        return abs(home_goals_diff)

    def __eq__(self, other):
        assert isinstance(other, GameWeekPrediction), (
            f"Can't compare {self.__class__.__name__} with {type(other).__name__}"
        )
        return(
            self.get_score() == other.get_score() and
            self.get_total_goals_diff() == other.get_total_goals_diff() and
            self.get_home_goals_diff() == other.get_home_goals_diff() and
            self.prediction_time == other.prediction_time
        )

    def __lt__(self, other):
        assert isinstance(other, GameWeekPrediction), (
            f"Can't compare {self.__class__.__name__} with {type(other).__name__}"
        )
        if self.get_score() != other.get_score():
            return self.get_score() < other.get_score()
        elif self.get_total_goals_diff() != other.get_total_goals_diff():
            return self.get_total_goals_diff() < other.get_total_goals_diff()
        elif self.get_home_goals_diff() != other.get_home_goals_diff():
            return self.get_home_goals_diff() < other.get_home_goals_diff()
        elif self.prediction_time != other.prediction_time:
            return self.prediction_time < other.prediction_time
        else:
            return False
