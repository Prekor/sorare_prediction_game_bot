from game_week_prediction import GameWeekPrediction
from game_week import GameWeek
from game_prediction import GamePrediction
from manager import Manager

from discord_parser.discord_parser import DiscordParser
from discord_parser.game_prediction_parser import GamePredictionParser
from discord_parser.manager_parser import ManagerParser


class GameWeekPredictionParser(DiscordParser):

    __BANK_GAME_COUNT = 1

    def __init__(self, ctx, message):
        super().__init__(ctx, message)
        self.predictions: list[GamePrediction] = []
        self.manager: Manager = ManagerParser(ctx, message).get_manager()

    def get_game_week_prediction(self, game_week: GameWeek) -> GameWeekPrediction:
        banked_games = 0
        assert self.ctx.message.created_at < game_week.deadline, (
            f"Submission deadline {game_week.deadline.strftime('%c')} has passed"
        )
        for line in self.message:
            prediction = GamePredictionParser().get_game_prediction(line, game_week.games)
            banked_games += int(prediction.bank)
            self.predictions.append(prediction)
        assert len(self.predictions) == len(game_week.games), f"There are not {len(game_week.games)} valid games"
        assert banked_games == self.__BANK_GAME_COUNT, f"There are {banked_games} bank game in the prediction"
        return GameWeekPrediction(self.ctx.message.created_at, self.predictions, self.manager)
