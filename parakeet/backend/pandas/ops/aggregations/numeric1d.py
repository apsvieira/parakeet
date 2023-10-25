from parakeet.core.ops.aggregations import Numeric1dFn, _Numeric1d


class PandasNumeric1d(_Numeric1d):
    def __init__(self, input_col: str, op: Numeric1dFn) -> None:
        super().__init__(input_col, op)

    @property
    def fn(self) -> callable:
        return str(self.op)
