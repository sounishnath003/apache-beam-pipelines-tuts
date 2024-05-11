from dataclasses import asdict
import json
import os
import time
import apache_beam as beam
from apache_beam.pipeline import Pipeline
from loguru import logger
from apache_beam.options.pipeline_options import PipelineOptions
import loguru

from etlpipelien.application.pipeline_options import CustomPipelineOptions
from etlpipelien.application.utils import (
    DataQualityCheckDoFn,
    ParseIntoJsonDoFn,
    load_schema,
)
from etlpipelien.application.utils import deserializer
from etlpipelien.domain.customer_model import Customer


def time_elapsed(func):
    def __wrapper__():
        start_time = time.time_ns()
        fn_output = func()
        end_time = time.time_ns()
        time_elapsed = round((end_time - start_time) / 1e9, 3)
        logger.info(f"{func} has been executed successfully...")
        logger.info(f"time elapsed: {time_elapsed} secs")
        return fn_output

    return __wrapper__


@time_elapsed
def run():
    # read the custom pipeline inputs
    custom_pipeline_opts = PipelineOptions().view_as(CustomPipelineOptions)
    logger.info(f"custom pipeline options={custom_pipeline_opts}")

    pipeline_opts = PipelineOptions()
    with Pipeline(options=pipeline_opts, argv=["--save_main_session=True"]) as pipeline:
        customer_schema = load_schema(custom_pipeline_opts.schema)
        logger.info(f"customer_schema: {customer_schema}")

        customer_pcol = (
            pipeline
            | "ReadCustomerCsv"
            >> beam.io.ReadFromText(
                custom_pipeline_opts.input_file, skip_header_lines=1
            )
            | "ParseIntoJson" >> beam.ParDo(ParseIntoJsonDoFn(schema=customer_schema))
            | "AvgSessionStrToFloat"
            >> beam.Map(
                lambda element: {
                    **element,
                    "avg_session_length": round(
                        float(element["avg_session_length"]), 3
                    ),
                }
            )
            | "TimeOnAppStrToFloat"
            >> beam.Map(
                lambda element: {
                    **element,
                    "time_on_app": round(float(element["time_on_app"]), 3),
                }
            )
            | "TimeOnWebSiteStrToFloat"
            >> beam.Map(
                lambda element: {
                    **element,
                    "time_on_website": round(float(element["time_on_website"]), 3),
                }
            )
            | "LengthOfMembershipStrToFloat"
            >> beam.Map(
                lambda element: {
                    **element,
                    "length_of_membership": round(
                        float(element["length_of_membership"]), 3
                    ),
                }
            )
            | "YearlySpendAmtStrToFloat"
            >> beam.Map(
                lambda element: {
                    **element,
                    "yearly_amount_spent": round(
                        float(element["yearly_amount_spent"]), 3
                    ),
                }
            )
        )
        customer_quality_checks_pcol = (
            customer_pcol
            | "Deserializer"
            >> beam.Map(
                lambda element: deserializer(schema_cls=Customer, element=element)
            ).with_output_types(Customer)
            | "DataQualityCheck"
            >> beam.ParDo(DataQualityCheckDoFn()).with_outputs(
                "failure", main="success"
            )
        )

        customer_quality_checks_pcol.success | "SerializeGood" >> beam.Map(
            lambda customer: asdict(customer)
        ) | "SaveGoodValues" >> beam.io.WriteToText(
            f"{custom_pipeline_opts.staging_folder}/good-outputs"
        )
        customer_quality_checks_pcol.failure | "SaveBadValues" >> beam.io.WriteToText(
            f"{custom_pipeline_opts.staging_folder}/bad-outputs"
        )

        pipeline.run()


if __name__ == "__main__":
    logger.info("pipeline is going to execute...")
    run()
