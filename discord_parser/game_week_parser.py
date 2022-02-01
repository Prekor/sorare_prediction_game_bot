import re
import datetime

from game import Game
from game_week import GameWeek
from prediction_exception import PredictionException
from discord_parser.discord_parser import DiscordParser
from discord_parser.game_parser import GameParser


class GameWeekParser(DiscordParser, GameParser):
    __NUMBER_OF_GAMES = 5
    def __init__(self, ctx):
        DiscordParser.__init__(self, ctx)
        GameParser.__init__(self)
        self.game_deadline_pattern = r"(?P<day>\d{2})(\/)(?P<month>\d{2})(\/)(?P<year>\d{4})(\s\-\s)(?P<hour>\d{2})(" \
                                     r"\:)(?P<minute>\d{2})"
        self.gw_number_pattern = r"(\#)(?P<gw_number>\d+)"

    def get_games(self) -> list[Game]:
        games: list[Game] = []
        for line in self.get_message_without_command():
            if re.search(self.game_deadline_pattern, line, re.IGNORECASE):
                continue
            game = self.get_game(line)
            if game:
                games.append(game)
        if len(games) != self.__NUMBER_OF_GAMES:
            raise PredictionException("There are not 5 valid games")
        return games

    def get_game_week_number(self) -> int:
        game_week_number = 0
        for line in self.get_message_without_command():
            if game_week_number == 0:
                gw_number_match = re.search(self.gw_number_pattern, line, re.IGNORECASE)
                if gw_number_match:
                    game_week_number = gw_number_match.group("gw_number")
                    return int(game_week_number)
        raise PredictionException("GameWeek number is missing")

    def get_deadline(self) -> datetime:
        submit_deadline = datetime.datetime.min
        for line in self.get_message_without_command():
            if submit_deadline == datetime.datetime.min:
                game_deadline_match = re.search(self.game_deadline_pattern, line, re.IGNORECASE)
                if game_deadline_match:
                    submit_deadline = datetime.datetime(
                        year=int(game_deadline_match.group("year")),
                        month=int(game_deadline_match.group("month")),
                        day=int(game_deadline_match.group("day")),
                        hour=int(game_deadline_match.group("hour")),
                        minute=int(game_deadline_match.group("minute"))
                    )
                    return submit_deadline
        raise PredictionException("Submit prediction deadline is missing")

    def get_game_week(self) -> GameWeek:
        game_week_number = self.get_game_week_number()
        deadline = self.get_deadline()
        games = self.get_games()
        return GameWeek(game_week_number, deadline, games)
