from dataclasses import dataclass


@dataclass
class TeamBestPasserStats:
    scorer_first_name: str
    scorer_last_name: str
    goals: int
    goal_assists: int
