import sqlite3
import os


DB_NAME = "data.db"
ABS_PATH_TO_DB_FOLDER = f'/home/{os.getlogin()}/.local/share/ptrack'
ABS_PATH_TO_DB_FILE = f'{ABS_PATH_TO_DB_FOLDER}/{DB_NAME}'


def close_db(
    con: sqlite3.connect(), cur: sqlite3.connect().cursor()
):
    print("close_db")
    con.commit()
    con.close()
    print("close_db closed")


def create_db(abs_path_to_file: str):
    print("create_db")
    try:
        con = sqlite3.connect(abs_path_to_file)
    except sqlite3.OperationalError:
        print("Folder isn't exist, create new folder")
        os.mkdir(ABS_PATH_TO_DB_FOLDER)
        return create_db(abs_path_to_file)
    print("sqlite3 is connected")

    cur = con.cursor()
    if cur.execute(
        "SELECT name FROM sqlite_master WHERE name = 'ptrack'"
    ).fetchone() is None:
        cur.execute("CREATE TABLE ptrack(date, name, title, time)")
        con.commit()
    print("create db closed")
    return con, cur


def get_json_from_specific_db_data(
    con: sqlite3.connect(), cur: sqlite3.connect().cursor(), date: str
):
    print("get_json_from_specific_db_data")
    _json = dict({date: [0, dict()]})
    # date, name, title, time
    for row in cur.execute(f'SELECT * FROM ptrack WHERE date IS \'{date}\''):
        if row[1] not in _json[row[0]][-1].keys():
            _json[row[0]][-1].update({row[1]: [0, dict()]})
        _json[row[0]][-1][row[1]][0] =\
            int(row[3]) + (_json[row[0]][1][row[1]])[0]
        _json[row[0]][0] += int(row[-1])
        _json[row[0]][-1][row[1]][-1].update({row[2]: int(row[3])})

    print("JSON was exported from db")

    print("get_json_from_specific_db_data closed")
    return _json


def get_json_from_all_db_data(  # REWRITE ( UNREADABLE CODE, EXCEPTION )
    con: sqlite3.connect(), cur: sqlite3.connect().cursor()
):
    print("get_json_from_all_db_data")
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

    print("get_json_from_all_db_data closed")
    return _json


def update_all_db(  # REWRITE ( UNREADABLE CODE, EXCEPTION )
    con: sqlite3.connect(), cur: sqlite3.connect().cursor(), _json: dict()
):
    print("update_all_db")
    for date in _json.keys():
        sum_all_name = sum([int(x[-1]) for x in cur.execute(f'''
SELECT * FROM ptrack WHERE date = \'{date}\'''')])
        if _json[date][0] == sum_all_name and len(_json[date][-1].keys()) != 1:
            continue
        for name in _json[date][-1].keys():
            for title in _json[date][-1][name][-1].keys():
                # print(f'iter {date} {name} {title}')  # debug
                sql_request = cur.execute('''
            SELECT * FROM ptrack WHERE\
            date IS ? AND name IS ? AND title IS ?
            ''', (date, name, title)).fetchone()
                if not sql_request:
                    # print("INSERT====")
                    cur.execute(
                        '''INSERT INTO ptrack VALUES (?, ?, ?, ?)''',
                        (date, name, title, _json[date][1][name][1][title]))
                    continue
                # print("UPDATE====")
                cur.execute('''UPDATE ptrack SET time = ?
                WHERE date = ? AND name = ? AND title = ? ''',
                ((_json[date][-1][name][-1][title] if
                  _json[date][-1][name][-1][title] > sql_request[-1]
                  else _json[date][-1][name][-1][title] + sql_request[-1]),
                 date, name, title))
        con.commit()
    print("update_all_db closed")


# _json[date][1][name][1][title]
def json_add_title(
    _json: dict, date: str, name: str, title: str, title_time: int
):
    print("json_add_title")
    if title not in _json[date][1][name][1].keys():
        _json[date][1][name][1].update({title: title_time})
    _json[date][0] += title_time
    _json[date][1][name][0] += title_time

    print("json_add_title closed")
    return _json


def json_add_name(
    _json: dict, date: str, name: str, title: str, title_time: int
):
    print("json_add_name")
    if date not in _json.keys():
        _json.update({date: [0, dict()]})
    if name not in _json[date][1].keys():
        _json[date][1].update({name: [title_time, dict()]})
    _json[date][1][name][1].update({title: title_time})
    _json[date][0] += title_time
    print("json_add_name closed")

    if (title and title_time):
        return json_add_title(_json, date, name, title, title_time)
    return _json
