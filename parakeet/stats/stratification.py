from dataclasses import dataclass

from numpy import log, where
from pandas import DataFrame

from parakeet.stats.cube import _INTERNAL_MARGINAL, Cube


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


def stratification(data: DataFrame, dims: list[str], label: str) -> Result:
    """Calculate the stratification of a data set.

    Parameters
    ----------
    data : DataFrame
        Input data set.
    dims : list[str]
        List of dimensions to stratify.
    label : str
        Label of the stratification.

    Returns
    -------
    Result
        Stratification result.

    """
    # Pre-aggregate statistics that are summarizable by sum.
    # This means that they can be aggregated by the cube op.
    basic_stats = (
        data[dims + [label]]
        .groupby(dims, observed=False, dropna=False)
        .agg(
            count=(label, "count"),
            zeros=(label, lambda x: (x == 0).sum()),
            ones=(label, lambda x: (x == 1).sum()),
        )
    )
    basic_stats = basic_stats.reset_index(drop=False)

    # Calculate and apply the cube op to fill in marginal values.
    cube = Cube(basic_stats, dims)
    stats = cube(basic_stats.drop(columns=dims)).fillna(0)

    # Calculate the remaining statistics as combinations of things
    # that can be aggregated by sum.
    #
    # This step would benefit from a more general solution.
    # Our previous solution was to define a desired schema for the
    # output and then calculate each column of the schema directly.
    # While it works, it has a few drawbacks:
    # 1. It's not very general. It's hard to extend to new statistics
    #    as you need to know how to calculate them from the basic stats.
    # 2. It can be less than ideal for performance due to duplicated
    #    calculations when more than one stat depends on any given op.
    # 3. It can lead to errors if the schema is not defined correctly.
    #    For example, if you forget to include a column in the schema
    #    that would be necessary for calculating another column.
    #
    # A better solution would be to define a schema for the output
    # and then resolve what needs to be calculated to obtain that schema.
    # This looks very much like defining a computation graph.
    # It goes from the label column, which can take some forms
    # (binary, categorical, continuous), to basic stats, to final stats.
    # In this scenario, basic statistics don't need to be defined explicitly and
    # don't need to be shown in the result set unless they are requested.
    population_idx = [_INTERNAL_MARGINAL] * len(dims)
    stats["zeros_pct"] = stats["zeros"] / stats["zeros"].loc[*population_idx]
    stats["ones_pct"] = stats["ones"] / stats["ones"].loc[*population_idx]
    stats["ones_ratio"] = stats["ones"] / stats["count"]
    stats["woe"] = log(stats["zeros"] / stats["ones"])
    stats["iv"] = (stats["zeros_pct"] - stats["ones_pct"]) * stats["woe"]
    return Result(stats)
