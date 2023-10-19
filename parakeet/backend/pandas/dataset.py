from collections import defaultdict
from typing import Dict, List, Optional, Set

from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy

from parakeet.core.dataset import Dataset, DType, Field, Fn, Schema


class PandasDataset(Dataset):
    def __init__(self, data: DataFrame, time: Optional[str] = None):
        self._data = data
        self._time = time

    @property
    def data(self):
        return self._data

    @property
    def schema(self) -> Schema:
        return [
            Field(name, _dtype_from_pandas(dtype))
            for (name, dtype) in self.data.dtypes.items()
        ]

    def shape(self):
        return self._data.shape

    @property
    def time(self):
        return self._time

    def groupby(self, by: List[str]) -> "Dataset":
        return PandasGroupByDataset(self._data.groupby(by), self._time)

    def agg(self, agg: List[Fn]) -> "Dataset":
        aggregations = _to_pandas_aggregations(agg)
        return PandasDataset(self._data.agg(aggregations), self._time)


class PandasGroupByDataset(Dataset):
    def __init__(self, data: DataFrameGroupBy, time: Optional[str] = None) -> None:
        self._data = data
        self._time = time

    @property
    def data(self):
        return self._data

    def schema(self) -> Schema:
        return [
            Field(c.name, _dtype_from_pandas(c.dtype.name)) for c in self.data.dtypes
        ]

    def shape(self):
        return self._data.shape

    @property
    def time(self):
        return self._time

    def groupby(self, _: List[str]) -> "Dataset":
        raise NotImplementedError("groupby is not supported for grouped dataset.")

    def agg(self, agg: List[Fn]) -> "Dataset":
        aggregations = _to_pandas_aggregations(agg)
        return PandasDataset(self._data.agg(aggregations), self._time)


def _dtype_from_pandas(dtype: str) -> DType:
    if dtype == "int64":
        return DType.INT64
    elif dtype == "float64":
        return DType.FLOAT64
    elif dtype == "object":
        return DType.STRING
    else:
        raise ValueError(f"Unknown dtype {dtype}")


def _to_pandas_aggregations(agg: List[Fn]) -> Dict[str, Set[callable]]:
    aggregations: Dict[str, Set[callable]] = defaultdict(set)
    for a in agg:
        if a.name in aggregations:
            raise ValueError(f"Duplicated aggregation {a.name()}.")

        aggregations[a.input_column].add(a.fn)

    return aggregations
