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
        self.manager: Manager = ManagerParser(ctx).parse()

    def parse(self, game_week: GameWeek) -> GameWeekPrediction:
        if self.ctx.message.created_at > game_week.deadline:
            err = "Deadline has passed" + str(game_week)
            raise PredictionException(err)
        for line in self.get_message_without_command():
            try:
                prediction = GamePredictionParser(self.ctx).parse(line, game_week)
            except PredictionException as err:
                # TODO: raise DiscordParseException instead of PredictionException
                pass
            else:
                self.predictions.append(prediction)
        return GameWeekPrediction(self.ctx.message.created_at, self.predictions, self.manager)
