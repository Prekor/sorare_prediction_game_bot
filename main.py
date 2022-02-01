import discord
from discord.ext import commands

from prediction_exception import PredictionException
from sorare_prediction_game import SorarePredictionGame
from discord_parser.game_week_parser import GameWeekParser
from discord_parser.game_week_prediction_parser import GameWeekPredictionParser
from discord_parser.game_week_closing_parser import GameWeekClosingParser
from secrets import *


class SorareDiscordPredictionGameBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")
        self.game: SorarePredictionGame or None = None

        @self.command(name='init_gw')
        async def init_game_week(ctx, *, args):
            try:
                game_week = GameWeekParser(ctx, args).get_game_week()
            except (PredictionException, AssertionError) as err:
                embed = discord.Embed(title="GameWeek initialization failed", color=discord.Color.red())
                embed.add_field(name="Error Message", value=str(err), inline=False)
            else:
                embed = discord.Embed(title="GameWeek initialization successful", color=discord.Color.green())
                embed.add_field(name="Registered Game Week", value=str(game_week), inline=False)
                # TODO : save game on disk using pickle
                self.game = SorarePredictionGame(game_week)
            await ctx.send(embed=embed)

        @self.command(name='submit')
        async def submit_prediction(ctx, *, args):
            try:
                assert self.game is not None, "There is no prediction game opened"
                assert self.game.game_week is not None, "There is no game week running in the prediction game"
                prediction = GameWeekPredictionParser(ctx, args).get_game_week_prediction(self.game.game_week)
            except (PredictionException, AssertionError) as err:
                await ctx.message.add_reaction('❌')
                embed = discord.Embed(title="Games submission failed", color=discord.Color.red())
                embed.add_field(name="Error Message", value=str(err), inline=False)
                await ctx.send(embed=embed)
            else:
                # TODO : save predictions using pickle
                self.game.add_prediction(prediction)
                await ctx.message.add_reaction('✅')

        @self.command(name='close_gw')
        async def close_game_week(ctx, *, args):
            try:
                assert self.game is not None, "There is no prediction game opened"
                assert self.game.game_week is not None, "There is no game week running in the prediction game"
                assert ctx.message.created_at >= self.game.game_week.deadline, (
                    f"Can't close the game before the deadline {self.game.game_week.deadline}"
                )
                GameWeekClosingParser(ctx, args).set_games_score(self.game.game_week.games)
                winner = self.game.get_winner()
            except (PredictionException, AssertionError) as err:
                embed = discord.Embed(title="Game closure failed", color=discord.Color.red())
                embed.add_field(name="Error Message", value=str(err), inline=False)
            else:
                await ctx.message.add_reaction('✅')
                embed = discord.Embed(title="Game Result", color=discord.Color.green())
                embed.add_field(
                    name=f"GW #{self.game.game_week.game_week_number} winner is :",
                    value=winner.name,
                    inline=False
                )
                # TODO: Verify that users still exist on the server
                # TODO: save closed game and predictions using pickle
                # TODO: Send log file
            await ctx.send(embed=embed)

        # @self.command(name='template')
        # async def get_template(ctx, *, args):
        #     pass


def main():
    bot = SorareDiscordPredictionGameBot()
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
