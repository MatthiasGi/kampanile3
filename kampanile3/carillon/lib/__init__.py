import time
from threading import Thread

import schedule

from ..models import Striker


def init_schedule():
    schedule.every().minute.at(":00").do(Striker.run_checks)

    def loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = Thread(target=loop, daemon=True)
    thread.start()
