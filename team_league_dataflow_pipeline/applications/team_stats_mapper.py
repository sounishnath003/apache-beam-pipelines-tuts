from typing import Dict
from dataclasses import dataclass
import dataclasses
import datetime
from team_league_dataflow_pipeline.domain.team_stats import TeamStats

from team_league_dataflow_pipeline.domain.team_stats_raw import TeamStatsRaw


def deserialize(team_stats_raw_as_dict: Dict) -> TeamStatsRaw:
    from dacite import from_dict

    return from_dict(data_class=TeamStatsRaw, data=team_stats_raw_as_dict)


def to_team_stats_bq(team_stats: TeamStats) -> Dict:
    team_stats_raw = dataclasses.asdict(team_stats)
    team_stats_raw.update({"ingestion_date": datetime.datetime.now().isoformat()})
    return team_stats_raw
