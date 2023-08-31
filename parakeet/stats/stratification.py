from dataclasses import dataclass

from pandas import DataFrame

from parakeet.stats.cube import _INTERNAL_MARGINAL


@dataclass
class Result:
    data: DataFrame

    def display(self) -> str:
        """Display the result with pretty formatting."""
        data = self.data.copy()
        data.columns = data.columns.str.replace("_", " ").str.title()
        data = data.round(3)
        data = data.rename(index={_INTERNAL_MARGINAL: "Total"})

        data = data.style.format(
            {
                "Count": "{:,.0f}",
                "Zeros": "{:,.0f}",
                "Ones": "{:,.0f}",
                "Zeros Pct": "{:.1%}",
                "Ones Pct": "{:.1%}",
                "Ones Ratio": "{:.1%}",
                "Woe": "{:.3f}",
                "Iv": "{:.3f}",
            }
        )

        return data
