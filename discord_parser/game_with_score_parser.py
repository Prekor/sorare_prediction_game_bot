import re

from game import Game


class GameWithScoreParser:
    def __init__(self):
        self.score_pattern = r"(\d+)\W*[:\-\–\_\;\/x\~]\W*(\d+)"

    def get_game_with_score(self, line: str, games: list[Game]) -> (Game, Game):
        game_with_score = None
        game_match = None
        for game in games:
            score_line = self.find_teams_in_line(game.home_team, game.away_team, line)
            if score_line is None:
                continue
            else:
                score = self.get_score(score_line)
                assert score is not None
                game_with_score = Game(game.home_team, game.away_team, score[0], score[1])
                game_match = game
                break
        assert game_with_score is not None
        assert game_match is not None
        # TODO handle raise exception when game doesn't match
        # TODO send template of the game
        return game_with_score, game_match

    @staticmethod
    def find_team_in_line(team: str, line: str):
        """"
         Searches every word of team name in line
         then removes the matched words from the line
         finally returns the remaining characters in line
        """
        team_found = False
        for split_team in team.split():
            if split_team in line:
                try:
                    line = line.replace(split_team, '', 1)
                    team_found = True
                except ValueError:
                    pass
        if not team_found:
            return None
        else:
            return line

    @staticmethod
    def find_teams_in_line(h_team: str, a_team: str, line: str):
        """"
         Searches and deletes home and away teams name in the line
         :return remaining characters if succeeds
         :return None otherwise
        """
        remaining_line = GameWithScoreParser.find_team_in_line(h_team, line)
        if remaining_line is None:
            return None
        return GameWithScoreParser.find_team_in_line(a_team, remaining_line)

    def get_score(self, line: str) -> (int, int):
        """"
         Searches score pattern in the line
         :return home goals and away goals if succeeds
         :return None otherwise
        """
        match_pattern = re.search(self.score_pattern, line, re.IGNORECASE)
        if match_pattern is None:
            return None
        else:
            return int(match_pattern.group(1)), int(match_pattern.group(2))
