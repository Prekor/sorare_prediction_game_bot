import discord
from discord.ext import commands

from gameweek import GameWeek
from game_week_prediction import GameWeekPrediction
from manager import Manager
from prediction_exception import PredictionException
from sorare_prediction_game import SorarePredictionGame
from discord_parser import game_week_prediction_parser
from secrets import *

BEST_CARD_EVER = "https://sorare.com/cards/javier-aldemar-zanetti-2009-limited-4"


class PredictionGameBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")
        self.game: SorarePredictionGame = None

        @self.command(name='init_gw')
        async def init_game_week(ctx, *, args):
            game_week = GameWeek()
            try:
                game_week.init_game_week(args)
            except PredictionException as err:
                embed = discord.Embed(title="Games submission failed", color=discord.Color.red())
                embed.add_field(name= "Error Message", value= str(err), inline=False)
            else:
                embed = discord.Embed(title="Games submission successful", color=discord.Color.green())
                embed.add_field(name= "Registered Game Week", value= str(game_week), inline=False)
                # TODO : save game_week on disk using pickle
                self.game = SorarePredictionGame(game_week)
            await ctx.send(embed=embed)

        @self.command(name='submit')
        async def submit_prediction(ctx, *, args):
            print(args)
            print(ctx.author)
            # print(ctx.guild.get_member_named(str(ctx.author)))
            print(ctx.message.created_at)

            assert(self.game is not None)
            assert(self.game.game_week is not None)

            try:
               prediction = game_week_prediction_parser(ctx, self.game.game_week)
            except PredictionException as err:
                pass
            else:
                self.game.add_prediction(prediction)

        # @self.command(name='close_gw')
        # async def close_game_week(ctx, *, args):
        #     print(args)
        #     TODO : Verify that users still exist on the server



def main():
    bot = PredictionGameBot()
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
