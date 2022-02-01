from game import Game
from game_prediction import GamePrediction

from discord_parser.game_with_score_parser import GameWithScoreParser


class GamePredictionParser(GameWithScoreParser):

    def __init__(self):
        super().__init__()
        self.game: Game or None = None

    def get_game_prediction(self, line: str, games: list[Game]) -> GamePrediction:
        game_with_score, self.game = self.get_game_with_score(line, games)
        assert game_with_score is not None
        assert self.game is not None
        return GamePrediction(
            self.game.home_team,
            self.game.away_team,
            game_with_score.home_goals,
            game_with_score.away_goals,
            self.is_bank(line),
            self.game
        )

    @staticmethod
    def is_bank(line):
        """"
         Searches specials characters that double game score
         :return True if found
         :return False otherwise
        """
        lower_line = line.lower()
        return (
                "bank" in lower_line or
                "building" in lower_line or
                "stadium" in lower_line or
                "house" in lower_line or
                ":bell:" in lower_line or
                "classical_building" in lower_line or
                "banker" in lower_line or
                "🏦" in line or
                "🏠" in line
        )
