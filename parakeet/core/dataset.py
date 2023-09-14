from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class DType(Enum):
    """Data type of a field."""

    INT32 = 1
    INT64 = 2
    FLOAT32 = 3
    FLOAT64 = 4
    STRING = 5
    BOOL = 6
    DATETIME = 7


@dataclass
class Field:
    """Field of a dataset."""

    name: str
    dtype: DType


Schema = List[Field]


class Fn(ABC):
    """Aggregation function."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the aggregation function."""

    @property
    @abstractmethod
    def fn(self) -> callable:
        """Return the function of the aggregation function.

        Here, we can think about `fn` as representing the name of an
        aggregation function, a function that calculates the aggregation,
        a function that returns a string, etc.
        """

    @property
    @abstractmethod
    def input_column(self) -> str:
        """Return the input columns of the aggregation function."""

    @abstractmethod
    def valid(self, input_schema: Schema) -> bool:
        """Check if the aggregation function is valid for the given schema."""

    @abstractmethod
    def output_dtype(self, input_schema: Schema) -> DType:
        """Output data type returned by the function."""


class Dataset(ABC):
    @property
    @abstractmethod
    def schema(self) -> Schema:
        """Retrieve the schema of the dataset."""

    @abstractmethod
    def shape(self) -> Tuple[int, int]:
        """Retrieve the shape of the dataset."""

    @property
    @abstractmethod
    def time(self) -> str:
        """Retrieve the time of the dataset."""

    @abstractmethod
    def groupby(self, by: List[str]) -> "Dataset":
        """Group by the given columns."""

    @abstractmethod
    def agg(self, agg: List[Fn]) -> "Dataset":
        """Aggregate the dataset."""
