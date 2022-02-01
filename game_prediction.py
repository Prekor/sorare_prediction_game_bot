from __future__ import annotations

from gameweek import GameWeek
from game import Game


class GamePrediction(Game):
    def __init__(self, h_team: str, a_team: str, h_goal: int, a_goal: int, bank: bool, game: Game):
        super().__init__(h_team, a_team, h_goal, a_goal)
        self.game: Game = game
        self.bank: bool = bank

    @staticmethod
    def create_from_line(line: str, game_week: GameWeek) -> GamePrediction:
        return GamePrediction()

    def get_result(self):
        pass

    def get_total_goals_diff(self) -> int:
        pass

    def get_home_goals_diff(self) -> int:
        pass