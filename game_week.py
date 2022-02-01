# -*- coding: utf-8 -*-
from datetime import datetime
from game import Game


class GameWeek:
    def __init__(self, game_week_number: int, deadline: datetime, games: list[Game]):
        self.game_week_number = game_week_number
        self.deadline = deadline
        self.games = games

    def __str__(self):
        reply_value = f"**GameWeek #{self.game_week_number}**\n"
        for game in self.games:
            reply_value += f"{game.home_team} - {game.away_team}\n"
        reply_value += "**Deadline CET Time**\n"
        reply_value += self.deadline.strftime("%c")
        return reply_value
