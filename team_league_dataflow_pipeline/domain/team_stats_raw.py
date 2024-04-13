from __future__ import annotations

from dataclasses import dataclass
from typing import List

from team_league_dataflow_pipeline.domain.exceptions.teams_stats_validation_exception import (
    TeamsStatsValidationException,
)

from team_league_dataflow_pipeline.domain.team_scorer_raw import TeamScorerRaw


TEAM_NAME_EMPTY_ERROR_TEXT = "Team name must not be empty or NULL"


@dataclass
class TeamStatsRaw:
    team_name: str
    team_score: int
    scorers: List[TeamScorerRaw]

    def validate_fields(self) -> TeamScorerRaw:
        if self.team_name is None or self.team_name == "":
            raise TeamsStatsValidationException([TEAM_NAME_EMPTY_ERROR_TEXT])

        return self
