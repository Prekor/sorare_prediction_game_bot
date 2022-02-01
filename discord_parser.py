# TODO : create one class for each parser, create discordParser class which contains the context
from discord.ext.commands import Context

from game_week_prediction import GameWeekPrediction
from game_prediction import GamePrediction
from gameweek import GameWeek
from manager import Manager
from prediction_exception import PredictionException


def game_week_prediction_parser(ctx: Context, game_week: GameWeek) -> GameWeekPrediction:
    predictions:list[GamePrediction] = []
    manager = manager_parser(ctx)
    for line in ctx.message.splitlines():
        try:
            prediction = game_prediction_parser(line, game_week)
        except PredictionException as err:
            pass
        else:
            predictions.append(prediction)
    return GameWeekPrediction(ctx.message.created_at, predictions, manager)


def game_week_parser():
    pass

def game_parser():
    pass

def game_prediction_parser(line: str, game_week: GameWeek) -> GamePrediction:
    return GamePrediction()

def manager_parser(ctx):
    return Manager(ctx.author)