from parakeet.core.ops.aggregations import Count


class PandasCount(Count):
    def __init__(self, name: str, input_col: str) -> None:
        super().__init__(name, input_col)

    @property
    def fn(self) -> callable:
        return "count"
