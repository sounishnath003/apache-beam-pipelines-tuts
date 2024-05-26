import logging
import apache_beam as beam
from apache_beam import DoFn, PTransform

from appp.libraries.helper import time_elapsed


class SplittingDoFn(DoFn):
    def __init__(self, staging_bucket: str):
        self.staging_bucket = staging_bucket

    def start_bundle(self):
        self.logger = logging.getLogger()

    def process(self, element: str, *args, **kwargs):
        # splitting the element by space
        tokens = element.split()
        self.logger.info("spliited.tokens=%s", tokens)
        return tokens


class SplittingPTransform(PTransform):

    def __init__(self, staging_bucket: str, label: str | None = None) -> None:
        super(SplittingPTransform, self).__init__(label)
        self.staging_bucket = staging_bucket

    @time_elapsed
    def expand(self, pcoll):
        processed_pcol = (
            pcoll
            | "SplitIntoTokens"
            >> beam.ParDo(SplittingDoFn(staging_bucket=self.staging_bucket))
            | "Flatten" >> beam.FlatMap(lambda row: [row])
        )

        processed_pcol | "WriteIntoBucket" >> beam.io.WriteToText(
            file_path_prefix=f"{self.staging_bucket}/flatten_tokens"
        )

        return processed_pcol
