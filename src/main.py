import subprocess
import datetime
import storage
from time import sleep, time


UPDATE_TIME = 300


def get_active_window_info():
    try:
        win_id = subprocess.check_output(
            ["xprop", "-root", "_NET_ACTIVE_WINDOW"]
        ).decode()
        win_id = win_id.split()[-1]
        if win_id == "0x0" or win_id == "found.":
            return None, None
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


if __name__ == '__main__':
    current_date = datetime.date.today().strftime("%d.%m.%Y")
    con, cur = storage.create_db(storage.ABS_PATH_TO_DB_FILE)
    beginning_time = time()
    json = storage.get_json_from_specific_db_data(con, cur, current_date)
    while True:
        app_name, title = get_active_window_info()
        if {app_name, title} == {None, None}:
            app_name, title = "Desktop", "None"

        # while i don't find best solution for more modest title name"
        title = "private"
        if app_name not in json[current_date][1].keys():
            storage.json_add_name(json, current_date, app_name, title, 1)
        elif title not in json[current_date][1][app_name][1].keys():
            storage.json_add_title(json, current_date, app_name, title, 1)
        else:
            json[current_date][0] += 1
            json[current_date][1][app_name][0] += 1
            json[current_date][1][app_name][1][title] += 1
            if int(time() - beginning_time) >= UPDATE_TIME:
                beginning_time = time()
                print(f'db update[{datetime.datetime.now().isoformat()}]')
                storage.update_all_db(con, cur, json)
        sleep(1)
