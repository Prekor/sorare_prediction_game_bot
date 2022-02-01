import re

from game import Game
from game_week import GameWeek
from game_prediction import GamePrediction

from discord_parser.discord_parser import DiscordParser


class GamePredictionParser(DiscordParser):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.game: Game or None = None

    def parse(self, line: str, game_week: GameWeek) -> GamePrediction:
        score_line: str = ""
        for game in game_week.games:
            score_line = GamePredictionParser.find_teams_in_line(game.home_team, game.away_team, line)
            if score_line is not None:
                self.game = game
                break

        assert(self.game is not None)
        home_goals, away_goals = GamePredictionParser.get_score(score_line)

        return GamePrediction(
            self.game.home_team,
            self.game.away_team,
            home_goals,
            away_goals,
            GamePredictionParser.is_bank(line),
            self.game
        )

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
        remaining_line = GamePredictionParser.find_team_in_line(h_team, line)
        if remaining_line is None:
            return None
        return GamePredictionParser.find_team_in_line(a_team, remaining_line)

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
