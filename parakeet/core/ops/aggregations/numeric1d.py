from enum import StrEnum, auto
from typing import List

from parakeet.core.dataset import DType, Fn, Schema


class Numeric1dFn(StrEnum):
    """Support 1-dimensional nueric aggregation functions.

    Quantile is not supported via this class, as it requires a parameter.
    """

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


class _Numeric1d(Fn):
    """Base class for numeric 1d aggregation functions.

    This class is used to represent aggregation functions that take a single
    column as input and return a single column as output.
    """

    def __init__(self, name: str, input_col: str, op: Numeric1dFn) -> None:
        self._name = name
        self._input_col = input_col
        self.op = op

    @property
    def name(self) -> str:
        return self._name

    @property
    def input_column(self) -> str:
        return self._input_col

    def valid(self, input_schema: Schema) -> bool:
        contained = self._input_col in [f.name for f in input_schema]
        supported_type = input_schema[self._input_col].dtype in {
            DType.INT64,
            DType.FLOAT64,
        }
        return contained and supported_type

    def output_dtype(self, input_schema: Schema) -> DType:
        return input_schema[self._input_col].dtype
