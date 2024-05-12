from pathlib import Path
from pkg_resources import resource_filename
from diablo2_mod_sql.data import D2StringTable, SelectStatement, UpdateStatement, InsertStatement


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

    stmt = UpdateStatement(tb, {
        'update': 'presence-states.json',
        'set': {'Key': {'literal': 'for_testing'}, 'enUS': 'zhCN'},
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

    c = stmt.execute()

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
    assert rows[0]['Key'] == 'for_testing'
    assert rows[1]['Key'] == 'for_testing'
    assert rows[0]['enUS'] == rows[0]['zhCN']
    assert rows[1]['enUS'] == rows[1]['zhCN']

    assert c == 2

    stmt = InsertStatement(tb, {
        'insert': 'presence-states.json',
        'columns': ['id', 'Key'],
        'query': {
            'select': [
                {'value': 88888},
                {'value': 'New_Item'}
            ]
        }
    })

    stmt.execute()

    stmt = SelectStatement(tb, {
        'select': '*',
        'from': 'presence-states.json'
    })

    rows = list(stmt.execute())

    assert len(rows) == 17
    assert rows[16]['id'] == 88888
    assert rows[16]['Key'] == 'New_Item'
