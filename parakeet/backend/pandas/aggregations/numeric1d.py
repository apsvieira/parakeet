from parakeet.core.ops.aggregations import Count, Numeric1dFn, _Numeric1d


class PandasNumeric1d(_Numeric1d):
    def __init__(self, name: str, input_col: str, op: Numeric1dFn) -> None:
        super().__init__(name, input_col, op)

    @property
    def fn(self) -> callable:
        return str(self.op)
