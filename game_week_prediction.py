from __future__ import annotations
from functools import total_ordering
from datetime import datetime

from game_prediction import GamePrediction
from manager import Manager


@total_ordering
class GameWeekPrediction:
    def __init__(self, prediction_time: datetime, game_predictions: list[GamePrediction], manager: Manager):
        self.game_prediction: list[GamePrediction] = game_predictions
        self.prediction_time: datetime = prediction_time
        self.manager: Manager = manager

    def get_result(self) -> int:
        pass

    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass