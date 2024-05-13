from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Union


class DataRow:
    _row: list
    _columns: tuple

    def __init__(self, row: list, columns: tuple):
        self._row = row
        self._columns = columns

    def __getitem__(self, key: Union[str, int]):
        if type(key) is str:
            return self._row[self._columns.index(key)]

        return self._row[key]

    def __setitem__(self, key: Union[str, int], value):
        if type(key) is str:
            key = self._columns.index(key)

        self._row[key] = value

    def __repr__(self):  # pragma: no cover
        return self._row.__repr__()


class DataTable(ABC):
    name: str
    path: Path
    columns: tuple
    rows: List[DataRow]

    @abstractmethod
    def __init__(self, path: Path):
        self.name = path.name
        self.path = path
