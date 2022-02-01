import re

from game import Game
from discord_parser.discord_parser import DiscordParser


class GameParser(DiscordParser):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.game_pattern = r"(?P<h_team>.*)(vs|\-|\–)(?P<a_team>.*)"
        self.score_pattern = r"(?P<h_team>.*)(vs|\-|\–)(?P<a_team>.*)(?P<h_goal>\d+)(\W*[\:\-])(?P<a_goal>\d+)"

    def get_game(self, line) -> Game or None:
        game_match = re.search(self.game_pattern, line, re.IGNORECASE)
        if not game_match:
            return None
        home_team = game_match.group("h_team").strip()
        away_team = game_match.group("a_team").strip()
        return Game(home_team, away_team)

    def get_game_score(self, line) -> Game or None :
        game_match = re.search(self.game_pattern, line, re.IGNORECASE)
        if not game_match:
            return None
        home_team = game_match.group("h_team").strip()
        away_team = game_match.group("a_team").strip()
        home_goals = int(game_match.group("h_goal"))
        away_team_goals = int(game_match.group("a_goal"))
        return Game(home_team, away_team, home_goals, away_team_goals)
