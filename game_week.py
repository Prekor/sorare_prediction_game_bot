# -*- coding: utf-8 -*-
from datetime import datetime
from game import Game


class GameWeek:
    def __init__(self, game_week_number: int, deadline: datetime, games: list[Game]):
        self.game_week_number = game_week_number
        self.deadline = deadline
        self.games = games

    def __str__(self):
        message = f"**GameWeek #{self.game_week_number}**\n"
        for game in self.games:
            message += f"{game.home_team} - {game.away_team}\n"
        message += "**Deadline CET Time**\n"
        message += self.deadline.strftime("%c")
        return message
