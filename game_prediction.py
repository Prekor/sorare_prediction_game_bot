# -*- coding: utf-8 -*-
from game import Game


class GamePrediction(Game):
    __BANK_FACTOR = 2
    __NO_BANK_FACTOR = 1
    __CORRECT_SCORE_POINTS = 4
    __CORRECT_RESULT_POINTS = 2

    def __init__(self, h_team: str, a_team: str, h_goal: int, a_goal: int, bank: bool, game: Game):
        super().__init__(h_team, a_team, h_goal, a_goal)
        self.bank: bool = bank
        self.bank_factor = self.__BANK_FACTOR if self.bank else self.__NO_BANK_FACTOR
        self.game = game

    def get_score(self) -> int:
        correct_score = self.home_goals == self.game.home_goals and self.away_goals == self.game.away_goals
        correct_result = self.get_result() == self.game.get_result()
        if correct_score:
            return self.__CORRECT_SCORE_POINTS * self.bank_factor
        elif correct_result:
            return self.__CORRECT_RESULT_POINTS * self.bank_factor
        else:
            return 0

    def get_total_goals_diff(self) -> int:
        return (self.game.home_goals + self.game.away_goals) - (self.home_goals - self.away_goals)

    def get_home_goals_diff(self) -> int:
        return self.game.home_goals - self.home_goals
