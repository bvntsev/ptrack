import subprocess
import datetime
import storage
from time import sleep, time


UPDATE_TIME = 600


def get_active_window_info():
    try:
        win_id = subprocess.check_output(
            ["xprop", "-root", "_NET_ACTIVE_WINDOW"]
        ).decode()
        win_id = win_id.split()[-1]
        if win_id == "0x0" or win_id == "found.":
            # Window is missing, probably background
            return "Desktop", "None"
        props = subprocess.check_output(
            ["xprop", "-id", win_id, "WM_CLASS", "WM_NAME"]
        ).decode()
        app, title = None, None
        for line in props.splitlines():
            if "WM_CLASS" in line:
                app = \
                line.split('=')[1].strip().split(",")[-1].strip().strip('"')
            elif "WM_NAME" in line:
                title = line.split('=')[1].strip().strip('"')
        return app, title
    except Exception:
        return None, None


def __update_db(
    con, cur, json: dict, beginning_time: float, current_date: str
):
    if int(time() - beginning_time) >= UPDATE_TIME \
        or current_date not in json.keys():
        beginning_time = time()
        print(f'db update[{datetime.datetime.now().isoformat()}]')
        storage.update_all_db(con, cur, json)
        json = dict({current_date: [0, dict()]})
    return json, beginning_time


if __name__ == '__main__':
    con, cur = storage.create_db(storage.ABS_PATH_TO_DB_FILE)
    beginning_time = time()
    json = dict({datetime.date.today().strftime("%d.%m.%Y"): [0, dict()]})

    while True:
        app_name, title = get_active_window_info()
        current_date = datetime.date.today().strftime("%d.%m.%Y")
        if current_date not in json.keys():
            json, beginning_time =\
                __update_db(con, cur, json, beginning_time, current_date)

        # while i don't find best solution for more modest title name"
        # title = "private"
        if app_name not in json[current_date][1].keys():
            storage.json_add_name(json, current_date, app_name, title, 1)
        elif title not in json[current_date][1][app_name][1].keys():
            storage.json_add_title(json, current_date, app_name, title, 1)
        else:
            json[current_date][0] += 1
            json[current_date][1][app_name][0] += 1
            json[current_date][1][app_name][1][title] += 1
            json, beginning_time =\
                __update_db(con, cur, json, beginning_time, current_date)
        sleep(1)
