import re
import datetime
from prediction_exception import PredictionException
from game import Game


class GameWeek:
    def __init__(self):
        self.games = []
        self.game_week_number = 0
        self.end_date_time = datetime.datetime.min

    def __str__(self):
        reply_value = f"**GameWeek #{self.game_week_number}**\n"
        for game in self.games:
            reply_value += f"{game.home_team} - {game.away_team}\n"
        reply_value += "**Deadline CET Time**\n"
        reply_value += self.end_date_time.strftime("%c")
        return reply_value

    # TODO : replace by staticmethod create_from_message
    def init_game_week(self, message):
        game_date_pattern = r"(?P<day>\d{2})(\/)(?P<month>\d{2})(\/)(?P<year>\d{4})(\s\-\s)" \
                            r"(?P<hour>\d{2})(\:)(?P<minute>\d{2})"
        game_pattern = r"(?P<h_team>.*)(vs|\-|\–)(?P<a_team>.*)"
        gw_number_pattern = r"(\#)(?P<gw_number>\d+)"
        for line in message.splitlines():
            game_date_match = re.search(game_date_pattern, line, re.IGNORECASE)
            game_match = re.search(game_pattern, line, re.IGNORECASE)
            gw_number_match = re.search(gw_number_pattern, line, re.IGNORECASE)
            if self.game_week_number == 0 and gw_number_match:
                self.game_week_number = gw_number_match.group("gw_number")
            elif self.end_date_time == datetime.datetime.min and game_date_match:
                self.end_date_time = datetime.datetime(
                    year=int(game_date_match.group("year")),
                    month=int(game_date_match.group("month")),
                    day=int(game_date_match.group("day")),
                    hour=int(game_date_match.group("hour")),
                    minute=int(game_date_match.group("minute"))
                )
            elif game_match:
                home_team = game_match.group("h_team").strip()
                away_team = game_match.group("a_team").strip()
                self.games.append(Game(home_team, away_team))
            else:
                # TODO : add line error in bot reply message
                raise PredictionException("Not handled yet")

        if self.game_week_number == 0:
            raise PredictionException("GameWeek number is missing")

        if self.end_date_time == datetime.datetime.min:
            raise PredictionException("Submit deadline is missing")

        if len(self.games) != 5:
            raise PredictionException("There are not 5 valid games")

        return True
