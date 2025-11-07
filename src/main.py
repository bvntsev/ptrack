import subprocess

def get_active_window_info():
    try:
        win_id = subprocess.check_output(
            ["xprop", "-root", "_NET_ACTIVE_WINDOW"]
        ).decode()
        win_id = win_id.split()[-1]
        if win_id == "0x0":
            return None

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
        return None

from time import sleep

if __name__ == '__main__':
    while True:
        print(get_active_window_info())
        sleep(1)

