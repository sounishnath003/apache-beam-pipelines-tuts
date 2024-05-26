import apache_beam as beam
from apache_beam import PTransform

from appp.libraries.helper import time_elapsed


class GroupByAnalyticsPTransform(PTransform):

    @time_elapsed
    def expand(self, pcoll):
        return (
            pcoll
            | "AddPair" >> beam.Map(lambda row: (row, 1))
            | "GroupByKey" >> beam.GroupByKey()
            | "Count" >> beam.CombineValues(beam.combiners.CountCombineFn())
        )
