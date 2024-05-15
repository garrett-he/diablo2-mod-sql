from pathlib import Path
from pkg_resources import resource_filename

import pytest
from diablo2_mod_sql.data import D2Database
from diablo2_mod_sql.data.d2string import D2StringTable
from diablo2_mod_sql.data.d2txt import D2TxtTable


@pytest.fixture(scope='module')
def d2database():
    return D2Database(Path(resource_filename('tests.res', 'data')))


@pytest.fixture(scope='function')
def presence_states_table():
    tb = D2StringTable(Path(resource_filename('tests.res', 'data/local/lng/strings/presence-states.json')))

    assert len(tb.rows) == 16
    assert tb.rows[0][0] == tb.rows[0]['id'] == 26047
    assert tb.rows[15][1] == tb.rows[15]['Key'] == 'presenceA5Hell'

    return tb


@pytest.fixture(scope='function')
def actinfo_table():
    tb = D2TxtTable(Path(resource_filename('tests.res', 'data/global/excel/actinfo.txt')))

    assert len(tb.rows) == 5
    return tb
