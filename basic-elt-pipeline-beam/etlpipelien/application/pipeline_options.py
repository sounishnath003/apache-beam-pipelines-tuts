from apache_beam.options.pipeline_options import _BeamArgumentParser, PipelineOptions


class CustomPipelineOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        parser.add_argument("--input_file", required=True, type=str)
        parser.add_argument("--schema", required=True, type=str)
        parser.add_argument("--bq_table", required=True, type=str)
        parser.add_argument("--staging_folder", required=True, type=str)
