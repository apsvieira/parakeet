from abc import ABC, abstractmethod
from typing import List

from parakeet.core.dataset import Dataset


class Engine(ABC):
    @abstractmethod
    def frequency(self, dataset: Dataset, dims: List[str]):
        """Calculate a frequency table for the given dimensions."""

    @abstractmethod
    def stratified(self, dataset: Dataset, dims: List[str], schema):
        """Calculate a set of metrics stratified by the given dimensions."""
