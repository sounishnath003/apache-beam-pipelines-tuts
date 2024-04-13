from __future__ import annotations
import random
from dacite import from_dict
import requests
from dataclasses import dataclass, replace
from typing import List
from team_league_dataflow_pipeline.domain.api_out_stats import ApiOutStats
from team_league_dataflow_pipeline.domain.team_best_passer_stats import (
    TeamBestPasserStats,
)
from team_league_dataflow_pipeline.domain.team_scorer_raw import TeamScorerRaw
from team_league_dataflow_pipeline.domain.team_stats_raw import TeamStatsRaw

from team_league_dataflow_pipeline.domain.team_top_scorer_stats import (
    TeamTopScorerStats,
)

TEAM_SLOGANS = {
    "PSG": "Paris est magique",
    "Real": "Hala Madrid",
    "Real2": "Hala Hala Madrid",
}


@dataclass
class TeamStats:
    team_name: str
    team_score: int
    team_total_goals: int
    team_slogan: int
    team_scorer_stats: TeamTopScorerStats
    best_passer_stats: TeamBestPasserStats
    api_out: ApiOutStats

    @staticmethod
    def compute_team_stats(team_stats_raw: TeamStatsRaw) -> TeamStats:
        team_scorers: List[TeamScorerRaw] = team_stats_raw.scorers
        top_scorer: TeamScorerRaw = max(
            team_scorers, key=lambda team_scorer: team_scorer.goals
        )
        best_passer: TeamScorerRaw = max(
            team_scorers, key=lambda team_scorer: team_scorer.goal_assists
        )

        team_total_goals: int = sum(map(lambda t: t.goals, team_scorers))

        top_scorer_stats = TeamTopScorerStats(
            first_name=top_scorer.scorer_first_name,
            last_name=top_scorer.scorer_last_name,
            goals=top_scorer.goals,
            games=top_scorer.games,
        )
        best_passer_stats = TeamBestPasserStats(
            scorer_first_name=best_passer.scorer_first_name,
            scorer_last_name=best_passer.scorer_last_name,
            goal_assists=best_passer.goal_assists,
            goals=best_passer.games,
        )

        return TeamStats(
            team_name=team_stats_raw.team_name,
            team_score=team_stats_raw.team_score,
            team_slogan="",
            team_total_goals=team_total_goals,
            team_scorer_stats=top_scorer_stats,
            best_passer_stats=best_passer_stats,
            api_out=None,
        )

    def add_slogan_to_stats(self) -> TeamStats:
        slogan: str = TEAM_SLOGANS.get(self.team_name)

        if slogan is None:
            raise AttributeError(f"No slogan found for the team: {self.team_name}")

        return replace(self, team_slogan=slogan)

    def call_api(self) -> TeamStats:
        uid = random.randint(a=1, b=10)
        api_out = requests.get(f"https://reqres.in/api/users/{uid}").json().get("data")
        api_out = from_dict(data_class=ApiOutStats, data=api_out)

        return replace(self, api_out=api_out)
