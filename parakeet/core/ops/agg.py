from typing import List

from parakeet.core.dataset import Dataset, Field, Fn, Schema
from parakeet.core.ops.op import Op


class Agg(Op):
    """Aggregation operation."""

    def __init__(self, agg: List[Fn]) -> None:
        if len(agg) == 0:
            raise ValueError("Aggregation list cannot be empty.")
        if len(agg) != len(set([a.name for a in agg])):
            raise ValueError("Aggregation list contains duplicate names.")
        self.agg = agg

    def transform(self, dataset: Dataset) -> Dataset:
        by = []
        if hasattr(dataset, "groups"):
            by = getattr(dataset, "groups")

        return dataset.agg(self._output_schema(dataset.schema, by))

    def _output_schema(self, input_schema: Schema, by: List[str]) -> Schema:
        if len(by) > 0:
            cols = [f.name for f in input_schema]
            not_contained = [c for c in by if c not in cols]
            if len(not_contained) > 0:
                raise ValueError(
                    f"Aggregation columns {not_contained} are not contained in the dataset"
                )

        invalid = [fn for fn in self.agg if not fn.valid(input_schema)]
        if len(invalid) > 0:
            raise ValueError(f"Invalid aggregation functions: {invalid}")

        by_fields = [f for f in input_schema if f.name in by]
        return by_fields + self.agg
