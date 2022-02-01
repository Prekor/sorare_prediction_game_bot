
class PredictionException(Exception):
    def __init__(self, message, template):
        super().__init__(message)
