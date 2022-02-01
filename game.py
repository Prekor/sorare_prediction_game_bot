# -*- coding: utf-8 -*-
from enum import Enum


class GameResult(Enum):
    """
    Allows easy comparison between
    manager predicted score and final game score
    """
    WIN = 1
    DRAW = 2
    LOSS = 3


class Game:
    def __init__(self, h_team: str, a_team: str, h_goal: int = 0, a_goal: int = 0):
        self.home_team = h_team
        self.away_team = a_team
        self.home_goals = h_goal
        self.away_goals = a_goal

    def set_score(self, h_goals: int, a_goals: int):
        self.home_goals = h_goals
        self.away_goals = a_goals

    def get_result(self):
        if self.home_goals > self.away_goals:
            return GameResult.WIN
        elif self.home_goals < self.away_goals:
            return GameResult.LOSS
        else:
            return GameResult.DRAW

    def __eq__(self, other):
        assert isinstance(other, Game)
        return self.home_team == other.home_team and self.away_team == other.away_team
