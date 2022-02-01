from prediction_exception import PredictionException
from discord_parser.game_week_parser import GameWeekParser

class GameWeek:
    def __init__(self, game_week_number, deadline, games):
        self.game_week_number = game_week_number
        self.deadline = deadline
        self.games = games

    def load_final_scores(self, ctx):
        game_week_parser = GameWeekParser(ctx)
        games_score = game_week_parser.get_games_score()
        for game in self.games:
            if game in games_score:
                game.update_score(games_score.game.home_goals, games_score.game.away_goals)
            else :
                raise PredictionException("There are not 5 valid games")

    def __str__(self):
        reply_value = f"**GameWeek #{self.game_week_number}**\n"
        for game in self.games:
            reply_value += f"{game.home_team} - {game.away_team}\n"
        reply_value += "**Deadline CET Time**\n"
        reply_value += self.deadline.strftime("%c")
        return reply_value
