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

    @staticmethod
    def get_result(h_goal, a_goal):
        if h_goal > a_goal:
            return GameResult.WIN
        elif h_goal < a_goal:
            return GameResult.LOSS
        else:
            return GameResult.DRAW

class Game:
    """
    Gets game teams and final score
    Calculates results from manager prediction
    """

    def __init__(self, h_team: str, a_team: str, h_goal: int = 0, a_goal: int = 0):
        self.home_team = h_team
        self.away_team = a_team
        self.home_goals = h_goal
        self.away_goals = a_goal
        self.result = GameResult.get_result(self.home_goals, self.away_goals)

    def update_score(self, h_goal: int, a_goal: int):
        self.home_goals = h_goal
        self.away_goals = a_goal
        self.result = GameResult.get_result(self.home_goals, self.away_goals)

    def get_game_results(self, other):
        """"
         Calculates, logs and returns all the manager game results for this game :
         score,
         total and home goals,
         global and home goal averages
         bank
        """
        if not isinstance(other, Game):
            return None
        score = 0
        total_goals_diff = (self.home_goals + self.away_goals) - (other.home_goals + other.away_goals)
        home_goals_diff = self.home_goals - other.home_goals

        if self.result == GameResult.get_result(other.home_goals, other.away_goals):
            if (other.home_goals == self.home_goals) and (other.away_goals == self.away_goals):
                score = 4
            else:
                score = 2
        return score, total_goals_diff, home_goals_diff,

    def __eq__(self, other):
        if isinstance(other, Game):
            if self.home_team == other.home_team and self.away_team == other.away_team:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return id(self)
