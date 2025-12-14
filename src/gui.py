from datetime import timedelta
import PyQt6
import matplotlib.pyplot as plt
import numpy as np
import storage


def td_from_sec(sec: int):
    return timedelta(seconds=sec)


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


def get_total_plot(_json: dict):
    con, cur = storage.create_db(storage.ABS_PATH_TO_DB_FILE)
    _json = storage.get_json_from_all_db_data(con, cur)

    y = np.array([((_json[x][0])) for x in
    _json.keys()])
    x = np.array([x for x in _json.keys()])
    print(y,x)

    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='date', ylabel='total time per day',
           title='Statistic for all time')
    ax.grid()

    plt.show()


json = dict()
get_total_plot(json)
#
# def Qt_launching():
#     pass
#
#


