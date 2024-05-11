from pathlib import Path
from pkg_resources import resource_filename
from diablo2_mod_sql.data import D2StringTable, SelectStatement


def test_data_table():
    filename = Path(resource_filename('tests.res', 'presence-states.json'))

    tb = D2StringTable(filename)

    stmt = SelectStatement(tb, {
        'select': '*',
        'from': 'presence-states.json',
        'where': {
            'or': [
                {
                    'eq': ['id', 26047]
                },
                {
                    'eq': ['id', 26048]
                }
            ]
        }
    })

    rows = list(stmt.execute())

    assert len(rows) == 2
    assert rows[0]['id'] == 26047
    assert rows[0]['Key'] == 'presenceMenus'
    assert rows[1]['id'] == 26048
    assert rows[1]['Key'] == 'presenceA1Normal'
