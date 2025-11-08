import sqlite3
import os
import json
from datetime import timedelta

DB_NAME = "data.db"
ABS_PATH_TO_DB_FOLDER = f'/home/{os.getlogin()}/.local/share/ptrack'
ABS_PATH_TO_DB_FILE = f'{ABS_PATH_TO_DB_FOLDER}/{DB_NAME}'


def create_db(path: str):
    print("open_bd")
    try:
        con = sqlite3.connect(path)
    except sqlite3.OperationalError:
        print("Folder isn't exist, create new folder")
        os.mkdir(ABS_PATH_TO_DB_FOLDER)
        return create_db(path)
    print("sqlite3 is connected")

    cur = con.cursor()
    if cur.execute(
        "SELECT name FROM sqlite_master WHERE name='ptrack'"
    ).fetchone() is None:
        cur.execute("CREATE TABLE ptrack(name, title, time)")
        con.commit()
    return con, cur


def td_from_isoformat(isoformat: str):
    return timedelta(
        hours=int(isoformat[:2]),
        minutes=int(isoformat[3:5]),
        seconds=int(isoformat[6:]),
    )


def unnecessery_zero(num):
    return str(num) if num >= 10 else '0' + str(num)


def isoformat_from_td(td: timedelta):
    td_sec = int(td.total_seconds())
    hours = unnecessery_zero(td_sec // 3600)
    minutes = unnecessery_zero(td_sec // 60 % 60)
    seconds = unnecessery_zero(
        td_sec - td_sec // 3600 * 3600 - td_sec // 60 % 60 * 60
    )
    return f'{hours}:{minutes}:{seconds}'


def get_json_from_db_data(con, cur):
    _json = dict()
    for row in cur.execute("SELECT name, title, time FROM ptrack"):
        if row[0] not in _json.keys():
            _json[row[0]] = list([
                row[2], list()
            ])
        else:
            _json[row[0]][0] = isoformat_from_td(
                td_from_isoformat(row[2]) + td_from_isoformat(_json[row[0]][0])
            )
        _json[row[0]][1].append({row[1]: row[2]})

    _json = json.dumps(_json)
    return _json


con, cur = create_db(ABS_PATH_TO_DB_FILE)


def update_db(
    con: sqlite3.connect(), cur: sqlite3.connect().cursor(), _json: dict()
):
    for iter in _json.keys():
        pass


_json = json.loads(get_json_from_db_data(con, cur))
update_db(con, cur, _json)
