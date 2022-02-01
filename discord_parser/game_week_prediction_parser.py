from game_week_prediction import GameWeekPrediction
from game_week import GameWeek
from game_prediction import GamePrediction
from manager import Manager

from discord_parser.discord_parser import DiscordParser
from discord_parser.game_prediction_parser import GamePredictionParser
from discord_parser.manager_parser import ManagerParser

from prediction_exception import PredictionException


class GameWeekPredictionParser(DiscordParser):
    def __init__(self, ctx, message):
        super().__init__(ctx, message)
        self.predictions: list[GamePrediction] = []
        self.manager: Manager = ManagerParser(ctx, message).get_manager()

    def get_game_week_prediction(self, game_week: GameWeek) -> GameWeekPrediction:
        assert self.ctx.message.created_at < game_week.deadline
        for line in self.message:
            try:
                prediction = GamePredictionParser().get_game_prediction(line, game_week.games)
            except PredictionException as err:
                # TODO: This should be a warning and not an error
                print(err)
            else:
                self.predictions.append(prediction)
        assert len(self.predictions) == len(game_week.games)
        assert not self.has_multiple_bank_games()
        assert not self.has_no_bank_game()
        return GameWeekPrediction(self.ctx.message.created_at, self.predictions, self.manager)

    def has_multiple_bank_games(self) -> bool:
        banked_games = 0
        if not self.predictions:
            return False
        for prediction in self.predictions:
            if prediction.bank:
                banked_games += 1
        if banked_games > 1:
            return True
        return False

    def has_no_bank_game(self) -> bool:
        if not self.predictions:
            return True
        for prediction in self.predictions:
            if prediction.bank:
                return False
        return True
