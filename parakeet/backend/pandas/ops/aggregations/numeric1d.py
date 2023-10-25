from parakeet.core.ops.aggregations import Numeric1dAggFn, _Numeric1dAgg


class PandasNumeric1d(_Numeric1dAgg):
    def __init__(self, input_col: str, op: Numeric1dAggFn) -> None:
        super().__init__(input_col, op)

    @property
    def fn(self) -> callable:
        # TODO: this is a gross approximation of the pandas API
        return str(self.op)
