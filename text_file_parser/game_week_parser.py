import re
import datetime

from game import Game
from game_week import GameWeek
from prediction_exception import PredictionException
from text_file_parser.text_file_parser import TextFileParser
from text_file_parser.game_parser import GameParser


class GameWeekParser(TextFileParser, GameParser):

    __NUMBER_OF_GAMES = 5
    __DEADLINE_FORMAT = "%d/%m/%Y - %H:%M"
    __GW_NUMBER_PATTERN = r"(\#)(?P<gw_number>\d+)"

    def __init__(self):
        TextFileParser.__init__(self)
        GameParser.__init__(self)

    def get_games(self) -> list[Game]:
        games: list[Game] = []
        for line in self.game_week_file:
            game = self.get_game(line)
            if game:
                games.append(game)
        if len(games) != self.__NUMBER_OF_GAMES:
            raise PredictionException("There are not 5 valid games")
        return games

    def get_game_week_number(self) -> int:
        game_week_number = 0
        for line in self.game_week_file:
            if game_week_number == 0:
                gw_number_match = re.search(self.__GW_NUMBER_PATTERN, line, re.IGNORECASE)
                if gw_number_match:
                    game_week_number = gw_number_match.group("gw_number")
                    return int(game_week_number)
        raise PredictionException("GameWeek number is missing")

    def get_deadline(self) -> datetime:
        submit_deadline = datetime.datetime.min
        for line in self.game_week_file:
            if submit_deadline == datetime.datetime.min:
                try:
                    submit_deadline = datetime.datetime.strptime(line, self.__DEADLINE_FORMAT)
                except ValueError:
                    pass
                else:
                    return submit_deadline
        raise PredictionException("Deadline for prediction submission is missing")

    def get_game_week(self) -> GameWeek:
        game_week_number = self.get_game_week_number()
        deadline = self.get_deadline()
        games = self.get_games()
        return GameWeek(game_week_number, deadline, games)
