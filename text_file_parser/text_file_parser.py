
class TextFileParser:
    __CURRENT_GW_RESULT_FILE = r".\text_file_parser\rsc\current_game_week\final_results.txt"
    __CURRENT_GW_PREDICTION_FILE = r".\text_file_parser\rsc\current_game_week\predictions.txt"

    def __init__(self):
        self.game_week_file: list[str] = []
        self.prediction_file: list[str] = []
        with open(self.__CURRENT_GW_RESULT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                self.game_week_file.append(line.strip())
        with open(self.__CURRENT_GW_PREDICTION_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                self.prediction_file.append(line.strip())
