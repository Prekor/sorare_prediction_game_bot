from game import Game

from discord_parser.discord_parser import DiscordParser
from discord_parser.game_with_score_parser import GameWithScoreParser


class GameWeekClosingParser(DiscordParser):
    def __init__(self, ctx, message):
        DiscordParser.__init__(self, ctx, message)

    def set_games_score(self, games: list[Game]) -> bool:
        for line in self.message:
            game_with_score, game_match = GameWithScoreParser.get_game_with_score(line, games)
            assert game_with_score is not None, f"No valid score found in:\n{line}"
            assert game_match is not None, f"There is no matching game in the game week for:\n{line}"
            game_match.set_score(game_with_score)
        return True
