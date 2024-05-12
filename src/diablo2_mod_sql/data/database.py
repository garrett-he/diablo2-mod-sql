from pathlib import Path
from .table import DataTable
from .d2string import D2StringTable


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
