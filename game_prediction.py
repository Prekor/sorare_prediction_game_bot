from __future__ import annotations

from game import Game


class GamePrediction(Game):
    def __init__(self, h_team: str, a_team: str, h_goal: int, a_goal: int, bank: bool):
        super().__init__(h_team, a_team, h_goal, a_goal)
        self.bank: bool = bank

    def get_total_goals_diff(self) -> int:
        pass

    def get_home_goals_diff(self) -> int:
        pass

    def get_game(self) -> Game:
        return Game(self.home_team, self.away_team, self.home_goals, self.away_goals)
