from typing import List


class TeamsStatsValidationException(Exception):
    def __init__(self, errors: List[str]) -> None:
        self.errors = errors
        super(TeamsStatsValidationException, self).__init__(self.errors)
