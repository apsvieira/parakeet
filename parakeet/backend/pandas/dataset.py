from typing import List, Optional

from pandas import DataFrame, NamedAgg
from pandas.core.groupby.generic import DataFrameGroupBy

from parakeet.core.dataset import Dataset, DesiredSchema, DType, Field, Fn, Schema

# TODO: We can later ensure that the desired schema is being followed
# by checking the schema of the resulting dataset versus the desired.


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
        return PandasGroupByDataset(self._data.groupby(by), self._time, self.schema)

    def agg(self, desired: DesiredSchema) -> "Dataset":
        aggregations = _to_pandas_aggregations(desired)
        return PandasDataset(self._data.agg(**aggregations), self._time)


class PandasGroupByDataset(Dataset):
    def __init__(
        self,
        data: DataFrameGroupBy,
        time: str,
        schema: Schema,
    ) -> None:
        self._data = data
        self._time = time
        self._schema = schema
        self.groups: List[str] = list(self._data.keys)

    @property
    def data(self):
        return self._data

    @property
    def schema(self) -> Schema:
        # TODO: should we mark the groupby columns as aggregated?
        return self._schema

    def shape(self):
        return self._data.shape

    @property
    def time(self):
        return self._time

    def groupby(self, _: List[str]) -> "Dataset":
        raise NotImplementedError("groupby is not supported for grouped dataset.")

    def agg(self, desired: DesiredSchema) -> "Dataset":
        aggregations = _to_pandas_aggregations(desired)
        return PandasDataset(self._data.agg(**aggregations), self._time)


def _dtype_from_pandas(dtype: str) -> DType:
    if dtype == "int64":
        return DType.INT64
    elif dtype == "float64":
        return DType.FLOAT64
    elif dtype == "object":
        return DType.STRING
    else:
        raise ValueError(f"Unknown dtype {dtype}")


def _to_pandas_aggregations(sch: Schema) -> List[NamedAgg]:
    return {
        f.name: NamedAgg(column=f.input_column, aggfunc=f.fn)
        for f in sch
        if isinstance(f, Fn)
    }
