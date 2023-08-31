from abc import ABC, abstractmethod
from typing import Dict, Tuple


class Dataset(ABC):
    @abstractmethod
    def schema(self) -> Dict[str, str]:
        """Retrieve the schema of the dataset."""

    @abstractmethod
    def shape(self) -> Tuple[int, int]:
        """Retrieve the shape of the dataset."""

    @property
    @abstractmethod
    def time(self) -> str:
        """Retrieve the time of the dataset."""
