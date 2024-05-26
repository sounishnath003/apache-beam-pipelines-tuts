import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from appp.libraries.helper import time_elapsed

from appp.libraries.splitting_ptransform import SplittingPTransform
from appp.libraries.aggregation_ptransform import GroupByAnalyticsPTransform


@time_elapsed
def main():
    pipeline_opts = PipelineOptions(save_main_session=True)
    with beam.Pipeline(options=pipeline_opts) as pipeline:
        (
            pipeline
            | "ReadInputs"
            >> beam.Create(
                ["Hello", "Hello good", "good day", "good morning", "Hello morning"]
            )
            | "TokenTransform"
            >> SplittingPTransform(
                staging_bucket="gs://sounish-cloud-workstation/dataflow/staging",
                label="tokenTransform",
            )
            | "GroupByTransactionPTranform"
            >> GroupByAnalyticsPTransform(label="groupByTransaction")
            | "WriteOutputs"
            >> beam.io.WriteToText(
                file_path_prefix="gs://sounish-cloud-workstation/dataflow/staging/tokens_out_analytics",
                file_name_suffix="_analytics.json",
                num_shards=1,
            )
        )

        pipeline.run().wait_until_finish()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
