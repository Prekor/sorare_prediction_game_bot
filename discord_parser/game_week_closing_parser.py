from game import Game

from discord_parser.discord_parser import DiscordParser
from discord_parser.game_with_score_parser import GameWithScoreParser


class GameWeekClosingParser(DiscordParser, GameWithScoreParser):
    def __init__(self, ctx, message):
        DiscordParser.__init__(self, ctx, message)
        GameWithScoreParser.__init__(self)

    def set_games_score(self, games: list[Game]) -> bool:
        # TODO : assert self.ctx.message.created_at >= game_week.deadline
        for line in self.message:
            game_with_score, game_match = self.get_game_with_score(line, games)
            assert game_with_score is not None
            assert game_match is not None
            # TODO handle raise exception when game doesn't match
            # TODO send template of the game
            game_match.home_goals = game_with_score.home_goals
            game_match.away_goals = game_with_score.away_goals
        return True
