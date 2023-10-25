from typing import List

from parakeet.core.dataset import Dataset, Schema
from parakeet.core.ops.op import Op


class GroupBy(Op):
    """Group By operation."""

    def __init__(self, by: List[str]) -> None:
        assert len(by) > 0
        assert len(by) == len(set(by))
        self.by = by

    def transform(self, dataset: Dataset) -> Dataset:
        cols = [f.name for f in dataset.schema]
        not_contained = [c for c in self.by if c not in cols]
        if len(not_contained) > 0:
            raise ValueError(
                f"Columns {not_contained} are not contained in the dataset."
            )

        return dataset.groupby(self.by)

    def _output_schema(self, input_schema: Schema) -> Schema:
        return input_schema
