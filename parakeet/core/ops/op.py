from abc import ABC, abstractmethod
from typing import List

from parakeet.core.dataset import Dataset, Schema


class Op(ABC):
    """Base operation performed on datasets."""

    @abstractmethod
    def transform(self, dataset: Dataset) -> Dataset:
        """Transform the given dataset."""

    @abstractmethod
    def output_schema(self, input_schema: Schema) -> Schema:
        """Return the schema of the output dataset."""


class Seq(Op):
    """Sequence of operations."""

    def __init__(self, ops: List[Op]) -> None:
        self._ops = ops

    def transform(self, dataset: Dataset) -> Dataset:
        """Apply operations sequentially."""
        for op in self._ops:
            dataset = op.transform(dataset)
        return dataset

    def output_schema(self, input_schema: Schema) -> Schema:
        schema = input_schema[:]
        for op in self._ops:
            schema = op.output_schema(schema)
        return schema
