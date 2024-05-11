from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Any

import mo_sql_parsing
from typing import Union, Iterable
from diablo2_mod_sql.operand import operand_map, Operand


class D2Database:
    base_dir: Path

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def get_table(self, path: str) -> DataTable:
        full_path = self.base_dir.joinpath(path)

        suffix = full_path.suffix.lower()

        if suffix == '.json':
            return D2StringTable(full_path)

        raise ValueError(full_path)

    def prepare(self, sql: str) -> SQLStatement:
        sql_tree = mo_sql_parsing.parse(sql.replace('/', '_'))

        if 'select' in sql_tree:
            stmt = SelectStatement(self.get_table(sql_tree['from'].replace('_', '/')), sql_tree)
        else:
            raise SyntaxError(sql)

        return stmt


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

    def __repr__(self):
        return self._row.__repr__()


class DataTable(ABC):
    columns: tuple
    rows: List[DataRow]

    @abstractmethod
    def __init__(self, path: Path):
        ...


class SQLStatement:
    table: DataTable
    where: Union[None, Operand]

    def __init__(self, table: DataTable, sql_tree: dict):
        self.table = table
        self.where = None

        if 'where' in sql_tree:
            self.where = self.parse_op_tree(sql_tree['where'])

    def parse_op_tree(self, op_tree: dict) -> Operand:
        op_code = next(iter(op_tree))
        result = operand_map[op_code]()

        for arg in op_tree[op_code]:
            if type(arg) is dict:
                if 'literal' in arg:
                    result.args.append({
                        'type': 'literal',
                        'value': arg['literal']
                    })
                else:
                    result.args.append({
                        'type': 'operand',
                        'value': self.parse_op_tree(arg)
                    })
            elif type(arg) is str:
                result.args.append({
                    'type': 'column',
                    'value': self.table.columns.index(arg)
                })
            else:
                result.args.append({
                    'type': 'literal',
                    'value': arg
                })

        return result


class SelectStatement(SQLStatement):
    def execute(self) -> Union[DataRow, Iterable[DataRow]]:
        if self.where is None:
            return self.table.rows

        return filter(lambda row: self.where.test(row), self.table.rows)


class D2StringTable(DataTable):
    def __init__(self, path: Path):
        self.columns = ('id', 'Key', 'enUS', 'zhTW', 'deDE', 'esES', 'frFR', 'itIT', 'koKR', 'plPL', 'esMX', 'jaJP', 'ptBR', 'ruRU', 'zhCN')

        self.rows = []

        with path.open('r', encoding='utf-8-sig') as fp:
            for row in json.load(fp):
                self.rows.append(DataRow(list(map(lambda col: row[col], self.columns)), self.columns))
