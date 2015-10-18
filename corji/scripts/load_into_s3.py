import threading
from queue import Queue

from corji.data_sources import(
    google_spreadsheets,
    s3
)
from corji.logging import Logger
from corji.settings import Config


logger = Logger(Config.LOGGER_NAME,
                Config.LOG_PATH,
                Config.LOG_NAME)
SPREADSHEET_URL = Config.SPREADSHEET_URL
corgis = {}


def worker():
    while True:
        item = queue.get()
        s3.put(item, corgis)
        queue.task_done()

# TODO: Better sysout. ("20% (9/180) complete, that kind of thing.")
if __name__ == "__main__":
    logger.debug("Spreadsheet URL defined: %s", SPREADSHEET_URL)

    google_spreadsheets.load(SPREADSHEET_URL)
    s3.load()
    corgis = google_spreadsheets.corgis

    queue = Queue()
    for corgi in corgis:
        queue.put(corgi)

    thread_count = 10
    for thread_num in range(thread_count):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
    queue.join()
