# -*- coding: utf-8 -*-
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
        has_multiple_bank_games = self.has_multiple_bank_games()
        for game_prediction in self.game_predictions:
            score += game_prediction.get_score(has_multiple_bank_games)
        return score

    def has_multiple_bank_games(self) -> bool:
        bank = 0
        for game_prediction in self.game_predictions:
            if game_prediction.bank:
                bank += 1
        return bank > 1

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
        assert isinstance(other, GameWeekPrediction)
        return(
            self.get_score() == other.get_score() and
            self.get_total_goals_diff() == other.get_total_goals_diff() and
            self.get_home_goals_diff() == other.get_home_goals_diff() and
            self.prediction_time == other.prediction_time
        )

    def __lt__(self, other):
        assert isinstance(other, GameWeekPrediction)
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
