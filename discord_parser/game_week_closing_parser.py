from game import Game

from discord_parser.discord_parser import DiscordParser
from discord_parser.game_with_score_parser import GameWithScoreParser


class GameWeekClosingParser(DiscordParser, GameWithScoreParser):
    def __init__(self, ctx):
        DiscordParser.__init__(self, ctx)
        GameWithScoreParser.__init__(self)

    @staticmethod
    def set_game_score(game_with_score: Game, games: list[Game]) -> bool:
        for game in games:
            if game == game_with_score:
                game.home_goals = game_with_score.home_goals
                game.away_goals = game_with_score.away_goals
                return True
        return False

    def set_games_score(self, games: list[Game]) -> bool:
        for line in self.get_message_without_command():
            game_with_score = self.get_game_with_score(line, games)
            assert game_with_score is not None
            assert self.set_game_score(game_with_score, games)
        return True
