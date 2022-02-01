import re

from game import Game


class GameWithScoreParser:

    __SCORE_PATTERN = r"(\d+)\W*[:\-\–\_\;\/x\~]\W*(\d+)"
    __GAME_CANCELLED = r"CANCELLED"

    @staticmethod
    def get_game_with_score(line: str, games: list[Game]) -> (Game, Game):
        game_with_score = None
        game_match = None
        for game in games:
            score_line = GameWithScoreParser.find_teams_in_line(game.home_team, game.away_team, line)
            if score_line is None:
                continue
            elif GameWithScoreParser.__GAME_CANCELLED.lower() in line.lower():
                game_with_score = Game(game.home_team, game.away_team, played=False)
                game_match = game
                break
            else:
                score = GameWithScoreParser.get_score(score_line)
                assert score is not None, f"No valid score found in:\n{line}"
                game_with_score = Game(game.home_team, game.away_team, score[0], score[1])
                game_match = game
                break
        assert game_with_score is not None, f"No valid score found in:\n{line}"
        assert game_match is not None, f"There is no matching game in the game week for:\n{line}"
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

    @staticmethod
    def get_score(line: str) -> (int, int):
        """"
         Searches score pattern in the line
         :return home goals and away goals if succeeds
         :return None otherwise
        """
        match_pattern = re.search(GameWithScoreParser.__SCORE_PATTERN, line, re.IGNORECASE)
        if match_pattern is None:
            return None
        else:
            return int(match_pattern.group(1)), int(match_pattern.group(2))
