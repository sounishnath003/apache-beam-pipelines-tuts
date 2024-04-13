import datetime
from typing import Dict
import logging
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from team_league_dataflow_pipeline.applications.team_league_options import (
    TeamLeauguePipelineOptions,
)
from team_league_dataflow_pipeline.applications.team_stats_mapper import (
    deserialize,
    to_team_stats_bq,
)
from team_league_dataflow_pipeline.domain.team_stats import TeamStats


def to_dict(message) -> Dict:
    return json.loads(message)


def main() -> None:
    logging.getLogger().setLevel(logging.INFO)

    team_league_options = PipelineOptions().view_as(TeamLeauguePipelineOptions)
    logging.info(f"team_league_options={team_league_options}")
    pipeline_opts = PipelineOptions()

    with beam.Pipeline(options=pipeline_opts) as pipeline:
        (
            pipeline
            | "Read JSON file"
            >> beam.io.ReadFromText(team_league_options.input_json_file)
            | "Map str message to dict" >> beam.Map(to_dict)
            | "Deserialize into domain dataclass" >> beam.Map(deserialize)
            | "Validate raw fields" >> beam.Map(lambda t: t.validate_fields())
            | "Compute team stats" >> beam.Map(TeamStats.compute_team_stats)
            | "Add Slogan" >> beam.Map(lambda t: t.add_slogan_to_stats())
            | "Add ApiStats out" >> beam.Map(lambda t: t.call_api())
            | "Map team stats to raw dict" >> beam.Map(to_team_stats_bq)
            | "Write to BigQuery"
            >> beam.io.WriteToBigQuery(
                project=team_league_options.project_id,
                dataset=team_league_options.team_leaugue_dataset,
                table=team_league_options.team_stats_table,
                method=team_league_options.bq_write_method,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            )
        )

        logging.info(
            f"dataflow job has been submitted on {datetime.datetime.now().isoformat()}"
        )


if __name__ == "__main__":
    main()
