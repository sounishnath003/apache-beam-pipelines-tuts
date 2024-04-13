from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TeamScorerRaw:
    scorer_first_name: str
    scorer_last_name: str
    goals: int
    goal_assists: int
    games: int
