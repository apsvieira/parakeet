"""Test cases for data cube operator.

These tests validate the implementation on the examples given in the original presentation, which can be found in [1]_.

References
----------
.. [1] http://dbpl2017.org/slides/DBPL-2017-5.pdf
"""

import pandas as pd
import pytest

from parakeet.stats.cube import _occurrence_matrix, Cube


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Model": ["Chevy", "Chevy", "Ford", "Ford", "Ford", "Ford"],
            "Year": [1990, 1990, 1990, 1990, 1991, 1991],
            "Color": ["Red", "Blue", "Green", "Blue", "Red", "Blue"],
            "Sale": [5, 87, 64, 99, 8, 7],
        }
    )


def testOccurrenceMatrixGeneration(sample_data):
    margin = "__all__"

    m1 = _occurrence_matrix(sample_data["Model"], margin)
    assert m1.shape == (3, 6)
    assert (m1.loc["Chevy"] == [1, 1, 0, 0, 0, 0]).all()
    assert (m1.loc["Ford"] == [0, 0, 1, 1, 1, 1]).all()
    assert (m1.loc[margin] == [1, 1, 1, 1, 1, 1]).all()

    m2 = _occurrence_matrix(sample_data["Year"], margin)
    assert m2.shape == (3, 6)
    assert (m2.loc[1990] == [1, 1, 1, 1, 0, 0]).all()
    assert (m2.loc[1991] == [0, 0, 0, 0, 1, 1]).all()
    assert (m2.loc[margin] == [1, 1, 1, 1, 1, 1]).all()

    m3 = _occurrence_matrix(sample_data["Color"], margin)
    assert m3.shape == (4, 6)
    assert (m3.loc["Red"] == [1, 0, 0, 0, 1, 0]).all()
    assert (m3.loc["Blue"] == [0, 1, 0, 1, 0, 1]).all()
    assert (m3.loc["Green"] == [0, 0, 1, 0, 0, 0]).all()
    assert (m3.loc[margin] == [1, 1, 1, 1, 1, 1]).all()


def testCubeCreation(sample_data):
    cube = Cube(sample_data, ["Year", "Color", "Model"])

    assert (cube.cube.loc[1990, "Red", "Chevy"] == [1, 0, 0, 0, 0, 0]).all()
    assert (cube.cube.loc[1990, "Blue", "Chevy"] == [0, 1, 0, 0, 0, 0]).all()
    assert (cube.cube.loc[1990, "Green", "Ford"] == [0, 0, 1, 0, 0, 0]).all()
    assert (cube.cube.loc[1990, "Blue", "Ford"] == [0, 0, 0, 1, 0, 0]).all()
    assert (cube.cube.loc[1991, "Red", "Ford"] == [0, 0, 0, 0, 1, 0]).all()
    assert (cube.cube.loc[1991, "Blue", "Ford"] == [0, 0, 0, 0, 0, 1]).all()
    assert (cube.cube.loc[1990, cube._marginal, "Chevy"] == [1, 1, 0, 0, 0, 0]).all()
    assert (cube.cube.loc[1990, cube._marginal, "Ford"] == [0, 0, 1, 1, 0, 0]).all()
    assert (cube.cube.loc[1991, cube._marginal, "Ford"] == [0, 0, 0, 0, 1, 1]).all()
    assert cube.cube.shape == (3 * 3 * 4, 6)

    sales = cube(sample_data[["Sale"]])
    assert (
        sales["Sale"]
        == [
            87,
            99,
            186,
            0,
            64,
            64,
            5,
            0,
            5,
            92,
            163,
            255,
            0,
            7,
            7,
            0,
            0,
            0,
            0,
            8,
            8,
            0,
            15,
            15,
            87,
            106,
            193,
            0,
            64,
            64,
            5,
            8,
            13,
            92,
            178,
            270,
        ]
    ).all()
