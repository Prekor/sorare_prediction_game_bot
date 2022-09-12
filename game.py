from __future__ import annotations
from enum import Enum


class GameResult(Enum):
    """
    Allows easy comparison between
    manager predicted score and final game score
    """
    WIN = 1
    DRAW = 2
    LOSS = 3
    CANCELLED = 4


class Game:
    def __init__(self, h_team: str, a_team: str, h_goal: int = 0, a_goal: int = 0, played: bool = True):
        self.home_team = h_team
        self.away_team = a_team
        self.home_goals = h_goal
        self.away_goals = a_goal
        self.played = played

    def __str__(self):
        return f"{self.home_team} - {self.away_team} : {self.home_goals}-{self.away_goals}"

    def get_result(self):
        if not self.played:
            return GameResult.CANCELLED
        elif self.home_goals > self.away_goals:
            return GameResult.WIN
        elif self.home_goals < self.away_goals:
            return GameResult.LOSS
        else:
            return GameResult.DRAW

    def set_score(self, game: Game):
        assert self.home_team == game.home_team, (
            f"Can't set score because {game.home_team} doesn't match {self.home_team}"
        )
        assert self.away_team == game.away_team, (
            f"Can't set score because {game.away_team} doesn't match {self.away_team}"
        )
        self.played = game.played
        self.home_goals = game.home_goals
        self.away_goals = game.away_goals
