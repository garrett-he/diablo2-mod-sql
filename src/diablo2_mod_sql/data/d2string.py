import json
from pathlib import Path
from .table import DataTable, DataRow


class D2StringTable(DataTable):
    def __init__(self, path: Path):
        self.columns = ('id', 'Key', 'enUS', 'zhTW', 'deDE', 'esES', 'frFR', 'itIT', 'koKR', 'plPL', 'esMX', 'jaJP', 'ptBR', 'ruRU', 'zhCN')

        self.rows = []

        with path.open('r', encoding='utf-8-sig') as fp:
            for row in json.load(fp):
                self.rows.append(DataRow(list(map(lambda col: row[col], self.columns)), self.columns))
