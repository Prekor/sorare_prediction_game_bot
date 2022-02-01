from game_week_prediction import GameWeekPrediction
from game_week import GameWeek
from game_prediction import GamePrediction
from manager import Manager

from discord_parser.discord_parser import DiscordParser
from discord_parser.game_prediction_parser import GamePredictionParser
from discord_parser.manager_parser import ManagerParser

from prediction_exception import PredictionException


class GameWeekPredictionParser(DiscordParser):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.predictions: list[GamePrediction] = []
        self.manager: Manager = ManagerParser(ctx).get_manager()

    def get_game_week_prediction(self, game_week: GameWeek) -> GameWeekPrediction:
        assert self.ctx.message.created_at < game_week.deadline
        for line in self.get_message_without_command():
            try:
                prediction = GamePredictionParser().get_game_prediction(line, game_week.games)
            except PredictionException as err:
                # TODO: This should be a warning and not an error
                print(err)
            else:
                self.predictions.append(prediction)
        assert len(self.predictions) == len(game_week.games)
        return GameWeekPrediction(self.ctx.message.created_at, self.predictions, self.manager)
