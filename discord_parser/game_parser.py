import re

from game import Game


class GameParser:
    def __init__(self):
        self.game_pattern = r"(?P<h_team>.*)(vs|\-|\–)(?P<a_team>.*)"

    def get_game(self, line) -> Game or None:
        game_match = re.search(self.game_pattern, line, re.IGNORECASE)
        if not game_match:
            return None
        home_team = game_match.group("h_team").strip()
        away_team = game_match.group("a_team").strip()
        return Game(home_team, away_team)
