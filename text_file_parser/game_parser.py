import re

from game import Game


class GameParser:
    def __init__(self):
        self.team_pattern = r"(?P<h_team>[A-Za-z].*)\W*(vs|\-|\–)\W*(?P<a_team>[A-Za-z].*)"
        self.score_pattern = r"(?P<score>((?P<h_goal>\d+)(\W*[\:\-])(?P<a_goal>\d+)|CANCELLED))"
        self.game_pattern = self.team_pattern + self.score_pattern

    def get_game(self, line) -> Game or None:
        game_match = re.search(self.game_pattern, line, re.IGNORECASE)
        if not game_match:
            return None
        home_team = game_match.group("h_team").strip()
        away_team = game_match.group("a_team").strip()
        return Game(home_team, away_team)
