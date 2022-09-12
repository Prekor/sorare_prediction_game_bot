from prediction_exception import PredictionException
from sorare_prediction_game import SorarePredictionGame

from text_file_parser.game_week_parser import GameWeekParser


class SorareDiscordPredictionGameTextFile:

    def __init__(self):
        self.game: SorarePredictionGame or None = None
        try:
            game_week = GameWeekParser().get_game_week()
        except (PredictionException, AssertionError) as err:
            print(err)
        else:
            self.game = SorarePredictionGame(game_week)

    def load_submitted_predictions(self):
        pass


def main():
    game = SorareDiscordPredictionGameTextFile()


if __name__ == "__main__":
    main()