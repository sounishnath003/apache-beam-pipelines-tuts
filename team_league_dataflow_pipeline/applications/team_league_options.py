import apache_beam as beam
from apache_beam.options.pipeline_options import _BeamArgumentParser, PipelineOptions


class TeamLeauguePipelineOptions(PipelineOptions):

    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        super()._add_argparse_args(parser)
        parser.add_argument(
            "--project_id", help="provide gcp project id", required=True
        )
        parser.add_argument(
            "--input_json_file", help="provide json file", required=True
        )
        parser.add_argument(
            "--input_subscription", help="provide input subscription", required=True
        )
        parser.add_argument(
            "--team_leaugue_dataset", help="provide team leaugue dataset", required=True
        )
        parser.add_argument(
            "--team_stats_table", help="provide team stats table", required=True
        )
        parser.add_argument(
            "--bq_write_method", help="provide bq write method", required=True
        )
