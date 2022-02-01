import discord
from discord.ext import commands
from gameweek import GameWeek
from exception import PredictionException
from secrets import *

BEST_CARD_EVER = "https://sorare.com/cards/javier-aldemar-zanetti-2009-limited-4"


class PredictionGameBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

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
            await ctx.send(embed=embed)

        # @self.command(name='close_gw')
        # async def close_game_week(ctx, *, args):
        #     print(args)


def main():
    bot = PredictionGameBot()
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
