from dataclasses import asdict, dataclass
import datetime
import json
from types import NoneType
import typing
from apache_beam import DoFn
from apache_beam import pvalue
from etlpipelien.domain.customer_model import Customer


from google.cloud import storage


def load_schema(gcs_path: str):
    """returns the loaded json schema from GCS bucket pattern"""
    bucket = gcs_path.split("/")[2]
    blob_name = "/".join(gcs_path.split("/")[3:])

    client = storage.Client()
    blob_file = client.get_bucket(bucket).get_blob(blob_name)
    return json.loads(blob_file.download_as_text(encoding="utf-8"))


class ParseIntoJsonDoFn(DoFn):
    """DoFn() class which converts the any CSV comma separated inputs into Parsable JSON string"""

    def __init__(self, schema, *unused_args, **unused_kwargs):
        super().__init__(*unused_args, **unused_kwargs)
        self.schema = schema

    def process(self, element, *args, **kwargs):
        # element will be the comma separated values
        elem_values = element.split(",")
        data_dict = dict()

        for sch, val in zip(self.schema, elem_values):
            if (
                val is None
                or len(val) == 0
                or val.lower() in ["null", "none", "na", ""]
            ):
                data_dict.update({sch["name"]: None})
            else:
                data_dict.update(
                    {sch["name"]: val.strip().replace('"', "").replace("'", "")}
                )

        yield data_dict


def deserializer(schema_cls: dataclass, element: typing.Dict):
    """returns the deserializer row and create the model.py object and return"""
    import dacite

    return dacite.from_dict(data_class=schema_cls, data=element)


class DataQualityCheckDoFn(DoFn):
    # regex hyper testing
    import re

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def process(self, element: Customer, *args, **kwargs):
        try:
            # Check the email regex pattern
            if self.EMAIL_REGEX.search(element.email) is None:
                raise ValueError("email id is not correct")

            yield pvalue.TaggedOutput("success", element)

        except Exception as e:  # Catching a broader exception
            elem_dict = asdict(element)
            elem_dict.update({"error": e.__str__()})
            elem_dict.update(
                {"date_inserted": datetime.date.today().strftime("%Y-%m-%d")}
            )

            yield pvalue.TaggedOutput("failure", elem_dict)
