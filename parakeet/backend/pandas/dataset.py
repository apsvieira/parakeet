from typing import Optional

from pandas import DataFrame

from parakeet.core.dataset import Dataset


class PandasDataset(Dataset):
    def __init__(self, data: DataFrame, time: Optional[str] = None):
        self._data = data
        self._time = time

    @property
    def data(self):
        return self._data

    def schema(self):
        return self._data.dtypes.to_dict()

    def shape(self):
        return self._data.shape

    @property
    def time(self):
        return self._time
