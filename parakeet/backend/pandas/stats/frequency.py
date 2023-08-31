"""Calculate frequency tables from Pandas datasets."""
from typing import List

from parakeet.backend.pandas.dataset import PandasDataset
from parakeet.stats.frequency import Result


def frequency(dataset: PandasDataset, dims: List[str]) -> Result:
    """Calculate the frequency of a data set.

    Parameters
    ----------
    dataset : PandasDataset
        Input data set.
    dims : list[str]
        List of dimensions to calculate the frequency of.

    Returns
    -------
    Result
        Frequency result.

    """
    freq = (
        dataset.data.groupby(dims, observed=False, dropna=False)
        .size()
        .reset_index()
        .rename(columns={0: "Frequency"})
    )
    freq["Percentage"] = freq["Frequency"] / freq["Frequency"].sum()
    return Result(freq, dims)
