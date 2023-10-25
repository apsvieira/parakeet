from typing import Callable, Optional

from parakeet.core.dataset import Dataset, DType
from parakeet.core.ops.op import Op as _Op


class LambdaOp(_Op):
    def __init__(
        self,
        fn: Callable[[Dataset, str, str], Dataset],
        input_column: str,
        output_dtype: DType,
        output_column: Optional[str],
    ) -> None:
        self.fn = fn
        self._input_column = input_column
        self._output_column = output_column
        self._output_column_dtype = output_dtype

    @property
    def input_column(self) -> str:
        return self._input_column

    @property
    def output_column(self) -> str:
        return self._output_column

    @property
    def output_column_dtype(self) -> DType:
        return self._output_column_dtype

    def transform(self, dataset: Dataset) -> Dataset:
        return self.fn(dataset, self._input_column, self._output_column)

    def _output_schema(self, input_schema: Dataset) -> Dataset:
        schema = input_schema[:]
        schema[self._output_column] = self._output_column_dtype
        return schema
