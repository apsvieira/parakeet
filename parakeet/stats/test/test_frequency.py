"""Test frequency table display functionality."""

import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from parakeet.core.order import OrderBy
from parakeet.stats.frequency import Result


def test_frequency_results_formatting():
    """Validate that results are correctly formatted to counts and percentages."""
    data = DataFrame(
        {
            "A": ["a", "a", "b", "b"],
            "B": ["c", "d", "c", "d"],
            "Frequency": [1, 2, 3, 4],
            "Percentage": [0.1, 0.2, 0.3, 0.4],
        }
    )
    result = Result(data, ["A", "B"])

    expected = DataFrame(
        {
            "A": ["a", "a", "b", "b"],
            "B": ["c", "d", "c", "d"],
            "Frequency": [1, 2, 3, 4],
            "Percentage": [0.1, 0.2, 0.3, 0.4],
            "Cumulative Frequency": [1, 3, 6, 10],
            "Cumulative Percentage": [0.1, 0.3, 0.6, 1.0],
        }
    )

    assert_frame_equal(result.display().data, expected)


def test_frequency_results_formatting_with_order_by():
    """Validate that results are correctly formatted to counts and percentages."""
    data = DataFrame(
        {
            "A": ["a", "a", "b", "b"],
            "B": ["c", "d", "c", "d"],
            "Frequency": [1, 2, 3, 4],
            "Percentage": [0.1, 0.2, 0.3, 0.4],
        }
    )
    result = Result(data, ["A", "B"])

    # Order by A ascending, B descending
    expected = DataFrame(
        {
            "A": ["a", "a", "b", "b"],
            "B": ["d", "c", "d", "c"],
            "Frequency": [2, 1, 4, 3],
            "Percentage": [0.2, 0.1, 0.4, 0.3],
            "Cumulative Frequency": [2, 3, 7, 10],
            "Cumulative Percentage": [0.2, 0.3, 0.7, 1.0],
        }
    )
    assert_frame_equal(result.display(OrderBy.from_str("A asc, B desc")).data, expected)

    # Order by A descending, B ascending
    expected = DataFrame(
        {
            "A": ["b", "b", "a", "a"],
            "B": ["c", "d", "c", "d"],
            "Frequency": [3, 4, 1, 2],
            "Percentage": [0.3, 0.4, 0.1, 0.2],
            "Cumulative Frequency": [3, 7, 8, 10],
            "Cumulative Percentage": [0.3, 0.7, 0.8, 1.0],
        }
    )
    assert_frame_equal(result.display(OrderBy.from_str("A desc, B asc")).data, expected)

    # Order by B ascending, A descending
    expected = DataFrame(
        {
            "A": ["b", "a", "b", "a"],
            "B": ["c", "c", "d", "d"],
            "Frequency": [3, 1, 4, 2],
            "Percentage": [0.3, 0.1, 0.4, 0.2],
            "Cumulative Frequency": [3, 4, 8, 10],
            "Cumulative Percentage": [0.3, 0.4, 0.8, 1.0],
        }
    )
    assert_frame_equal(result.display(OrderBy.from_str("B asc, A desc")).data, expected)

    # Order by B descending, A ascending
    expected = DataFrame(
        {
            "A": ["a", "b", "a", "b"],
            "B": ["d", "d", "c", "c"],
            "Frequency": [2, 4, 1, 3],
            "Percentage": [0.2, 0.4, 0.1, 0.3],
            "Cumulative Frequency": [2, 6, 7, 10],
            "Cumulative Percentage": [0.2, 0.6, 0.7, 1.0],
        }
    )
    assert_frame_equal(result.display(OrderBy.from_str("B desc, A asc")).data, expected)

    # Order by Frequency ascending
    expected = DataFrame(
        {
            "A": ["a", "a", "b", "b"],
            "B": ["c", "d", "c", "d"],
            "Frequency": [1, 2, 3, 4],
            "Percentage": [0.1, 0.2, 0.3, 0.4],
            "Cumulative Frequency": [1, 3, 6, 10],
            "Cumulative Percentage": [0.1, 0.3, 0.6, 1.0],
        }
    )
    assert_frame_equal(result.display(OrderBy.from_str("Frequency asc")).data, expected)

    # Order by Frequency descending
    expected = DataFrame(
        {
            "A": ["b", "b", "a", "a"],
            "B": ["d", "c", "d", "c"],
            "Frequency": [4, 3, 2, 1],
            "Percentage": [0.4, 0.3, 0.2, 0.1],
            "Cumulative Frequency": [4, 7, 9, 10],
            "Cumulative Percentage": [0.4, 0.7, 0.9, 1.0],
        }
    )
    assert_frame_equal(
        result.display(OrderBy.from_str("Frequency desc")).data, expected
    )

    # Order by Percentage ascending
    expected = DataFrame(
        {
            "A": ["a", "a", "b", "b"],
            "B": ["c", "d", "c", "d"],
            "Frequency": [1, 2, 3, 4],
            "Percentage": [0.1, 0.2, 0.3, 0.4],
            "Cumulative Frequency": [1, 3, 6, 10],
            "Cumulative Percentage": [0.1, 0.3, 0.6, 1.0],
        }
    )
    assert_frame_equal(
        result.display(OrderBy.from_str("Percentage asc")).data, expected
    )

    # Order by Percentage descending
    expected = DataFrame(
        {
            "A": ["b", "b", "a", "a"],
            "B": ["d", "c", "d", "c"],
            "Frequency": [4, 3, 2, 1],
            "Percentage": [0.4, 0.3, 0.2, 0.1],
            "Cumulative Frequency": [4, 7, 9, 10],
            "Cumulative Percentage": [0.4, 0.7, 0.9, 1.0],
        }
    )
    assert_frame_equal(
        result.display(OrderBy.from_str("Percentage desc")).data, expected
    )
