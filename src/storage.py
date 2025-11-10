import sqlite3
import os
# import json


DB_NAME = "data.db"
ABS_PATH_TO_DB_FOLDER = f'/home/{os.getlogin()}/.local/share/ptrack'
ABS_PATH_TO_DB_FILE = f'{ABS_PATH_TO_DB_FOLDER}/{DB_NAME}'


def create_db(abs_path_to_file: str):
    print("open_bd")
    try:
        con = sqlite3.connect(abs_path_to_file)
    except sqlite3.OperationalError:
        print("Folder isn't exist, create new folder")
        os.mkdir(ABS_PATH_TO_DB_FOLDER)
        return create_db(abs_path_to_file)
    print("sqlite3 is connected")

    cur = con.cursor()
    if cur.execute(
        "SELECT name FROM sqlite_master WHERE name='ptrack'"
    ).fetchone() is None:
        cur.execute("CREATE TABLE ptrack(date, name, title, time)")
        con.commit()
    return con, cur


def get_json_from_db_data(  # REWRITE ( UNREADABLE CODE, EXCEPTION )
    con: sqlite3.connect(), cur: sqlite3.connect().cursor(), date: str
):
    _json = dict()
    # date, name, title, time
    for row in cur.execute('SELECT * FROM ptrack'):
        if row[0] not in _json.keys():
            _json[row[0]] = [0, {row[1]: [row[3], dict()]}]
        else:
            if row[1] not in _json[row[0]][-1].keys():
                _json[row[0]][-1].update({row[1]: [0, dict()]})
            _json[row[0]][-1][row[1]][0] =\
                int(row[3]) + (_json[row[0]][1][row[1]])[0]
        _json[row[0]][0] += int(row[-1])
        _json[row[0]][-1][row[1]][-1].update({row[2]: int(row[3])})

    print("JSON was exported from db")
    return _json


def update_all_db(  # REWRITE ( UNREADABLE CODE, EXCEPTION )
    con: sqlite3.connect(), cur: sqlite3.connect().cursor(), _json: dict()
):
    for date in _json.keys():
        sum_all_title = sum([int(x[-1]) for x in cur.execute(f'''\
SELECT * FROM ptrack WHERE date = \'{_json[date][0]}\' AND name = \'{date}\'\
            ''')])
        if _json[date][0] == sum_all_title:
            continue
        for name in _json[date][-1].keys():
            for title in _json[date][-1][name][-1].keys():
                # print(f'iter {date} {name} {title}')  # debug
                if _json[date][-1][name][-1][title] != cur.execute(f'\
            SELECT * FROM ptrack WHERE\
            date IS \'{date}\' AND name IS \'{name}\' AND title IS \'{title}\''
                ).fetchone()[-1]:
                    # print(f'Changed {date} {name} {title}')  # debug
                    cur.execute(f'\
            UPDATE ptrack SET time = {_json[date][-1][name][-1][title]} WHERE\
            date = \'{date}\' AND name = \'{name}\' AND title = \'{title}\'')
        con.commit()


# def json_add_new_title(_json: dict, _row: Row):  # FIX
#     _json[_row.name][-1].append([_row.title, _row.title_time])
#     _json[_row.name][1] += _row.title_time
#     return _json


# def json_add_new_row(_json: dict, _row: Row):  # FIX
#     _json[_row.name] =\
#         [_row.date, _row.title_time, [_row.title, _row.title_time]]
#     return _json


# def json_update(
#     name: str, date: str, total_time: int, title: str, title_time: int
# ):
#     pass
