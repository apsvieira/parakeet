from dataclasses import dataclass
from typing import List, Optional

from pandas import DataFrame

from parakeet.core.order import OrderBy


@dataclass
class Result:
    data: DataFrame
    dims: List[str]

    def display(self, order_by: Optional[OrderBy] = None) -> str:
        """Display the result with pretty formatting."""
        if order_by is None:
            order_by = OrderBy.from_dimensions(self.dims, True)
        data = self.data.copy()
        data.columns = data.columns.str.replace("_", " ").str.title()

        cols, ascending = order_by.to_pandas()
        data = data.sort_values(by=cols, ascending=ascending)
        data["Cumulative Frequency"] = data["Frequency"].cumsum()
        data["Cumulative Percentage"] = data["Percentage"].cumsum()

        data = data.style.format(
            {
                "Frequency": "{:,.0f}",
                "Percentage": "{:.2%}",
                "Cumulative Frequency": "{:,.0f}",
                "Cumulative Percentage": "{:.2%}",
            }
        )

        return data
