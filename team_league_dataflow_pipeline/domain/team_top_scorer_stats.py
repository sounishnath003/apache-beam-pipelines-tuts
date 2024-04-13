from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TeamTopScorerStats:
    first_name: str
    last_name: str
    goals: int
    games: int
