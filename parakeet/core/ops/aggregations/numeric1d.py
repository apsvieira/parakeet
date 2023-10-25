from enum import StrEnum, auto

from parakeet.core.dataset import DType, Fn, Schema


class Numeric1dAggFn(StrEnum):
    """Support 1-dimensional numeric aggregation functions with no arguments."""

    COUNT = auto()
    CUMSUM = auto()
    MAX = auto()
    MEAN = auto()
    MEDIAN = auto()
    MIN = auto()
    MODE = auto()
    NUNIQUE = auto()
    STD = auto()
    SUM = auto()
    VAR = auto()


class _Numeric1dAgg(Fn):
    """Base class for numeric 1d aggregation functions.

    This class is used to represent aggregation functions that take a single
    column as input and return a single column as output.
    """

    def __init__(self, input_col: str, op: Numeric1dAggFn) -> None:
        self._input_col = input_col
        self.op = op

    @property
    def name(self) -> str:
        return f"{self.op.name.upper()}({self._input_col})"

    @property
    def input_column(self) -> str:
        return self._input_col

    def valid(self, input_schema: Schema) -> bool:
        idx = _find(input_schema, self._input_col)
        supported_type = input_schema[idx].dtype in {
            DType.INT64,
            DType.FLOAT64,
        }
        return idx >= 0 and supported_type

    def output_dtype(self, input_schema: Schema) -> DType:
        idx = _find(input_schema, self._input_col)
        return input_schema[idx].dtype


def _find(iterable, value) -> int:
    """Find the index of the first occurence of value in iterable."""
    for i, v in enumerate(iterable):
        if v.name == value:
            return i
    return -1
