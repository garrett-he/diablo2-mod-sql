from __future__ import annotations
from typing import Union, Iterable
from abc import ABC, abstractmethod
import mo_sql_parsing
from diablo2_mod_sql.data import D2Database
from diablo2_mod_sql.data.table import DataTable, DataRow
from diablo2_mod_sql.sql.operand import operand_map, Operand

table_mask = {
    '/': '__SEP__',
    '-': '__HYPHEN__'
}


def mask_table_name(sql: str) -> str:
    for k, v in table_mask.items():
        sql = sql.replace(k, v)

    return sql


def unmask_table_name(name: str) -> str:
    for k, v in table_mask.items():
        name = name.replace(v, k)

    return name


def parse(db: D2Database, sql: str) -> SQLStatement:
    sql_tree = mo_sql_parsing.parse(mask_table_name(sql))

    if 'select' in sql_tree:
        stmt = SelectStatement(db.get_table(unmask_table_name(sql_tree['from'])), sql_tree)
    else:
        raise SyntaxError(sql)

    return stmt


class SQLStatement(ABC):
    table: DataTable
    where: Union[None, Operand]
    sql_tree: dict

    def __init__(self, table: DataTable, sql_tree: dict):
        self.table = table
        self.where = None
        self.sql_tree = sql_tree

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

    @abstractmethod
    def execute(self):
        ...


class SelectStatement(SQLStatement):
    def execute(self) -> Union[DataRow, Iterable[DataRow]]:
        if self.where is None:
            return self.table.rows

        return filter(lambda row: self.where.test(row), self.table.rows)


class UpdateStatement(SQLStatement):
    set: dict

    def __init__(self, table: DataTable, sql_tree: dict):
        super().__init__(table, sql_tree)

        if 'set' in sql_tree:
            self.set = sql_tree['set']

    def execute(self) -> int:
        i = 0

        for row in self.table.rows:
            if self.where is not None and not self.where.test(row):
                continue

            for key in self.set:
                value = self.set[key]

                if type(value) is dict and 'literal' in value:
                    row[key] = value['literal']
                else:
                    row[key] = row[value]

            i += 1

        return i


class InsertStatement(SQLStatement):
    def execute(self) -> None:
        row = [''] * len(self.table.columns)

        for i in range(len(self.sql_tree['query']['select'])):
            if 'columns' in self.sql_tree:
                column_index = self.table.columns.index(self.sql_tree['columns'][i])
            else:
                column_index = i

            row[column_index] = self.sql_tree['query']['select'][i]['value']

        self.table.rows.append(DataRow(row, self.table.columns))


class DeleteStatement(SQLStatement):
    def execute(self) -> int:
        i = len(self.table.rows)

        if self.where is None:
            self.table.rows = []

            return i

        self.table.rows = [row for row in self.table.rows if not self.where.test(row)]

        return i - len(self.table.rows)
