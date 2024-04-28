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

    # preparing for dummy data
    # Sample data for demonstration (replace with your actual database reading logic)
    data1 = [
        {"key1": "A", "key2": "X", "value": 10},
        {"key1": "A", "key2": "Y", "value": 20},
        {"key1": "B", "key2": "X", "value": 15},
    ]

    data2 = [
        {"key1": "A", "key2": "X", "value": 30},
        {"key1": "B", "key2": "Y", "value": 25},
    ]

    data3 = [
        {"key1": "A", "key2": "X", "value": 5},
        {"key1": "B", "key2": "X", "value": 10},
    ]

    combined_data = [
        {"key1": "A", "key2": "X", "value": 5},
        {"key1": "B", "key2": "X", "value": 10},
        {"key1": "A", "key2": "X", "value": 30},
        {"key1": "B", "key2": "Y", "value": 25},
        {"key1": "A", "key2": "X", "value": 10},
        {"key1": "A", "key2": "Y", "value": 20},
        {"key1": "B", "key2": "X", "value": 15},
    ]

    with beam.Pipeline(options=pipeline_opts) as pipeline:
        # read the frames into pcol
        pcol1 = (
            pipeline
            | "Read data1" >> beam.Create(data1)
            | beam.Map(lambda x: ((x["key1"], x["key2"]), x["value"]))
        )
        pcol2 = (
            pipeline
            | "Read data2" >> beam.Create(data2)
            | beam.Map(lambda x: ((x["key1"], x["key2"]), x["value"]))
        )
        pcol3 = (
            pipeline
            | "Read data3" >> beam.Create(data3)
            | beam.Map(lambda x: ((x["key1"], x["key2"]), x["value"]))
        )

        # perform the joining of the datasets
        joined_pcol = (
            {"pcol1": pcol1, "pcol2": pcol2, "pcol3": pcol3}
        ) | "merge" >> beam.CoGroupByKey()

        # aggregate data
        aggregated_pcol = joined_pcol | "aggregate data" >> beam.Map(
            lambda element: dict(
                key1=element[0][0],
                key2=element[0][0],
                total_value=sum(sum(sublist) for sublist in element[1].values()),
            )
        )
        # aggregated data
        (aggregated_pcol | "printer" >> beam.Map(logging.info))
        logging.info("======== DONE =========")
        # combined 3 pcols
        npcol1 = (
            pipeline
            | "Read ndata1" >> beam.Create(data1)
            | "map-to-row-encode1"
            >> beam.Map(
                lambda row: beam.Row(
                    key1=row["key1"],
                    key2=row["key2"],
                    value=row["value"],
                    key12=f'{row["key1"]}-{row["key2"]}',
                )
            )
        )
        npcol2 = (
            pipeline
            | "Read ndata2" >> beam.Create(data2)
            | "map-to-row-encode2"
            >> beam.Map(
                lambda row: beam.Row(
                    key1=row["key1"],
                    key2=row["key2"],
                    value=row["value"],
                    key12=f'{row["key1"]}-{row["key2"]}',
                )
            )
        )
        npcol3 = (
            pipeline
            | "Read ndata3" >> beam.Create(data3)
            | "map-to-row-encode3"
            >> beam.Map(
                lambda row: beam.Row(
                    key1=row["key1"],
                    key2=row["key2"],
                    value=row["value"],
                    key12=f'{row["key1"]}-{row["key2"]}',
                )
            )
        )
        combined_npcol = [npcol1, npcol2, npcol3] | beam.Flatten()
        (
            combined_npcol
            | "groupby"
            >> beam.GroupBy("key12").aggregate_field(
                field="value", combine_fn=sum, dest="total_value"
            )
            | "clog" >> beam.Map(logging.info)
        )

        logging.info(
            f"dataflow job has been submitted on {datetime.datetime.now().isoformat()}"
        )


if __name__ == "__main__":
    main()
