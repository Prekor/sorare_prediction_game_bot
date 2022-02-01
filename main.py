import discord
from discord.ext import commands

from game_week import GameWeek
from prediction_exception import PredictionException
from sorare_prediction_game import SorarePredictionGame
from discord_parser.game_week_prediction_parser import GameWeekPredictionParser
from discord_parser.game_week_parser import GameWeekParser
from secrets import *

BEST_CARD_EVER = "https://sorare.com/cards/javier-aldemar-zanetti-2009-limited-4"


class PredictionGameBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")
        self.game: SorarePredictionGame = None

        @self.command(name='init_gw')
        async def init_game_week(ctx, *, args):
            try:
                game_week = GameWeekParser.get_game_week(ctx)
            except PredictionException as err:
                embed = discord.Embed(title="Games submission failed", color=discord.Color.red())
                embed.add_field(name="Error Message", value=str(err), inline=False)
            else:
                embed = discord.Embed(title="Games submission successful", color=discord.Color.green())
                embed.add_field(name="Registered Game Week", value=str(game_week), inline=False)
                # TODO : save game_week on disk using pickle
                self.game = SorarePredictionGame(game_week)
            await ctx.send(embed=embed)

        @self.command(name='submit')
        async def submit_prediction(ctx, *, args):
            assert(self.game is not None)
            assert(self.game.game_week is not None)

            try:
                prediction = GameWeekPredictionParser(ctx).parse(self.game.game_week)
            except PredictionException as err:
                pass
                # await ctx.args.add_reaction('❎')
            else:
                self.game.add_prediction(prediction)
                # await ctx.args.add_reaction('✅')

        @self.command(name='close_gw')
        async def close_game_week(ctx, *, args):
            assert(self.game is not None)
            assert(self.game.game_week is not None)
            try:
                self.game.game_week.load_final_scores(ctx)
            except PredictionException as err:
                pass
            else:
                winner = self.game.get_winner()
                embed = discord.Embed(title="Game Result", color=discord.Color.green())
                embed.add_field(
                    name=f"GW #{self.game.game_week.game_week_number} winner is :",
                    value=winner.name,
                    inline=False
                )
        #     TODO : Verify that users still exist on the server


def main():
    bot = PredictionGameBot()
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
