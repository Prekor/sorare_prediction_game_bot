import re

from manager import Manager
from text_file_parser.text_file_parser import TextFileParser


class GameWeekSubmittedPredictionsParser(TextFileParser):
    __NAME_PATTERN = r'(?P<name>.*)(\s\—\s)(Hier|Aujourd|\d{2}/\d{2}/\d{4})'

    def __init__(self):
        TextFileParser.__init__(self)
        self.submitted_predictions: dict[Manager, list[str]] = {}

    def get_manager_name(self, line: str):
        """"
         Searches manager name in line
         :return @ + manager name if found
         :return None otherwise
        """
        name_match = re.search(self.__NAME_PATTERN, line)
        if name_match is None:
            return None
        else:
            return "@" + name_match.group("name")

    def get_game_week_submitted_predictions(self):
        manager_name = None
        for line in self.prediction_file:
            name = self.get_manager_name(line)
            if name is not None:
                manager_name = name
                self.submitted_predictions[Manager(manager_name)] = []
            else:
                if manager_name is not None:
                    self.submitted_predictions[Manager(manager_name)].append(line)
