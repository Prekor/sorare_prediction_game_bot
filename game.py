# -*- coding: utf-8 -*-

from enum import Enum
import re


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

    @staticmethod
    def filter_team_name(team_name: str) -> str:
        """"
         Removes common club name suffixes such as FC, AC, SC
         and by using split method make sure that others elements
         of the team name remain are not altered
        """
        name_suffixes = ["AC", "AS", "CF", "FC", "SC", "SCO", "FK", "FF", "KP"]
        split_name = team_name.lower().split()
        for suffix in name_suffixes:
            if suffix.lower() in split_name:
                try:
                    split_name.remove(suffix.lower())
                except ValueError:
                    pass
        return " ".join(split_name)

    @staticmethod
    def find_team_in_line(team: str, line: str):
        """"
         Searches every word of team name in line
         then removes the matched words from the line
         finally returns the remaining characters in line
        """
        team_found = False
        for split_team in team.split():
            if split_team in line:
                try:
                    line = line.replace(split_team, '', 1)
                    team_found = True
                except ValueError:
                    pass
        if not team_found:
            return None
        else:
            return line

    @staticmethod
    def find_teams_in_line(h_team: str, a_team: str, line: str):
        """"
         Searches and deletes home and away teams name in the line
         :return remaining characters if succeeds
         :return None otherwise
        """
        remaining_line = Game.find_team_in_line(h_team, line)
        if remaining_line is None:
            return None
        return Game.find_team_in_line(a_team, remaining_line)

    @staticmethod
    def get_score(line: str):
        """"
         Searches score pattern in the line
         :return home goals and away goals if succeeds
         :return None otherwise
        """
        score_pattern = r"(\d+)\W*[:\-\–\_\;\/x\~]\W*(\d+)"
        match_pattern = re.search(score_pattern, line, re.IGNORECASE)
        if match_pattern is None:
            return None
        else:
            return int(match_pattern.group(1)), int(match_pattern.group(2))

    def get_game_score(self, line: str):
        """"
         Searches home and away teams name in the line
         and then gets the predicted score
         :return home goals and away goals if succeeds
         :return None otherwise
        """
        h_team = Game.filter_team_name(self.home_team)
        a_team = Game.filter_team_name(self.away_team)
        score_line = Game.find_teams_in_line(h_team, a_team, line.lower())
        if score_line is None:
            return None
        return Game.get_score(score_line)

    @staticmethod
    def is_bank(line):
        """"
         Searches specials characters that double game score
         :return True if found
         :return False otherwise
        """
        lower_line = line.lower()
        return "bank" in lower_line or "building" in lower_line or \
               "stadium" in lower_line or "house" in lower_line or \
               "home" in lower_line or ":bell:" in lower_line or \
               "classical_building" in lower_line or "banker" in lower_line or "🏦" in line or "🏠" in line

    def calculate_game_results(self, h_goals: int, a_goals: int, bank: bool):
        """"
         Calculates, logs and returns all the manager game results for this game :
         score,
         total and home goals,
         global and home goal averages
         bank
        """
        total_goals = h_goals + a_goals
        g_avg = self.global_goal_avg - total_goals
        home_g_avg = self.home_goals - h_goals
        bank_msg_logger = ""
        bank_game = 0
        score = 0

        if self.result == GameResult.get_result(h_goals, a_goals):
            if (h_goals == self.home_goals) and (a_goals == self.away_goals):
                score = 4
            else:
                score = 2
        no_bank_score = score
        if bank:
            score *= 2
            bank_msg_logger = " #BANK# "
            bank_game = 1
        return score, no_bank_score, total_goals, h_goals, g_avg, home_g_avg, bank_game

    def get_game_results(self, line: str):
        """"
         Gets manager results for this game
         :return all results if game matched
         :return None otherwise
        """
        game_score = self.get_game_score(line.lower())
        if game_score is None:
            return None
        else:
            return self.calculate_game_results(*game_score, Game.is_bank(line))
