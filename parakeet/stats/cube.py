from typing import Any
from scipy.linalg import khatri_rao
import numpy as np
import pandas as pd
from itertools import product


class Cube:
    """Definition of a data cube operator.

    Performs cubing operation as described in [1]_.

    References
    ----------
    .. [1] Macedo, H.D., Oliveira, J.N., "A linear algebra approach to OLAP."
        Form Asp Comp 27, 283–307 (2015).
        https://doi.org/10.1007/s00165-014-0316-9
    """

    def __init__(self, data: pd.DataFrame, dims: list, agg: str = "sum"):
        """Constructor method.

        Parameters
        ----------
        data : np.array
            Input data array.
        dims : list
            List of dimensions to cube.
        agg : str, optional
            Aggregation function, by default "sum".
        """
        self.dims = dims
        self.agg = agg
        self._marginal = "__all__"

        # Calculate the cube operator from input data dimensions
        cube = None
        occurrence_matrices = {
            dim: _occurrence_matrix(data[dim], self._marginal) for dim in dims
        }
        dims = self.dims[::-1]
        for dim in dims:
            m = occurrence_matrices[dim]
            if cube is None:
                cube = m
            else:
                cube = indexed_khatri_rao(m, cube)
        self.cube = cube

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        # Open question: how can this be applied to other operations that not sum?
        return self.cube @ data


def _occurrence_matrix(s: pd.Series, _marginal: str) -> pd.DataFrame:
    """Calculate the occurrence matrix for a dimension.

    Parameters
    ----------
    s : pd.Series
        Input data series.
    _marginal : str
        Representation of the marginal dimension.

    Returns
    -------
    pd.DataFrame
        Occurrence matrix.
    """

    m = pd.get_dummies(s, drop_first=False)
    m[_marginal] = 1
    m = m.astype(int).T
    m.index.name = s.name
    return m


def indexed_khatri_rao(m1: pd.DataFrame, m2: pd.DataFrame) -> pd.DataFrame:
    """Calculate the indexed Khatri-Rao product of two matrices.

    Parameters
    ----------
    m1 : pd.DataFrame
        First input matrix.
    m2 : pd.DataFrame
        Second input matrix.

    Returns
    -------
    pd.DataFrame
        Indexed Khatri-Rao product.
    """

    # Create a MultiIndex with the combinations of unique values.
    # We directly use the MultiIndex constructor instead of pd.MultiIndex.from_product
    # because the latter does not handle tuple expansion to yield flat tuples.
    index = pd.MultiIndex.from_tuples(
        list(
            product(
                *[m1.index.get_level_values(name).unique() for name in m1.index.names]
                + [m2.index.get_level_values(name).unique() for name in m2.index.names]
            )
        ),
        names=[*m1.index.names, *m2.index.names],
    )
    # Calculate the Khatri-Rao product
    kr = khatri_rao(m1, m2)

    # Create a new dataframe with the multiindex and the kr product
    return pd.DataFrame(kr, index=index, columns=range(kr.shape[1]))
