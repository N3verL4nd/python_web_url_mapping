from admin import is_admin, relaunch_as_admin
from ui import launch_ui
from web_server import stop_web_server
import atexit
import signal
import sys

PORT = 8080

def cleanup():
    stop_web_server(PORT)

def main():
    if not is_admin():
        relaunch_as_admin()
        return

    atexit.register(cleanup)
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    launch_ui()

if __name__ == "__main__":
    main()
