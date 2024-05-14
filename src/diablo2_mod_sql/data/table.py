from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Union, Iterator
from enum import Enum
from dataclasses import dataclass
from collections.abc import Iterable


class DataColumnType(Enum):
    BOOLEAN = 'bool'
    INTEGER = 'int'
    FLOAT = 'float'
    STRING = 'str'


@dataclass
class DataColumn:
    name: str
    type: DataColumnType


class DataColumnCollection(Iterable):
    columns: List[DataColumn]

    def __init__(self, specs: list[dict] = None):
        self.columns = []

        if specs is not None:
            for spec in specs:
                self.columns.append(DataColumn(name=spec['name'], type=spec['type']))

    def index(self, name: str) -> int:
        return next(i for i, col in enumerate(self.columns) if col.name == name)

    def __iter__(self) -> Iterator[DataColumn]:
        return iter(self.columns)

    def __len__(self):
        return len(self.columns)

    def __getitem__(self, key: Union[str, int]):
        if type(key) is str:
            return self.columns[self.index(key)]

        return self.columns[key]


class DataRow:
    _row: List[Union[bool, int, float, str]]
    _columns: DataColumnCollection

    def __init__(self, row: list, columns: DataColumnCollection):
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

    def __len__(self):
        return len(self._row)


class DataTable(ABC):
    name: str
    path: Path
    columns: DataColumnCollection
    rows: List[DataRow]

    @abstractmethod
    def __init__(self, path: Path):
        self.name = path.name
        self.path = path

    def __post_init__(self):
        for row in self.rows:
            for i in range(len(row)):
                if self.columns[i].type == DataColumnType.INTEGER:
                    row[i] = int(row[i])
                elif self.columns[i].type == DataColumnType.FLOAT:
                    row[i] = float(row[i])
                elif self.columns[i].type == DataColumnType.BOOLEAN:
                    row[i] = bool(row[i])
                elif self.columns[i].type == DataColumnType.STRING:
                    row[i] = str(row[i])
