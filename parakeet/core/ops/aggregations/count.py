from typing import List

from parakeet.core.dataset import DType, Fn, Schema


class Count(Fn):
    def __init__(self, name: str, input_col: str) -> None:
        self._name = name
        self._input_col = input_col

    @property
    def name(self) -> str:
        return self._name

    @property
    def input_columns(self) -> List[str]:
        return [self._input_col]

    def valid(self, input_schema: Schema) -> bool:
        return self._input_col in [f.name for f in input_schema]

    def output_dtype(self, input_schema: Schema) -> DType:
        return DType.INT64
