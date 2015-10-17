from collections import Counter

from tabulate import tabulate

from corji.data_sources import google_spreadsheets
from corji.logging import Logger
from corji.settings import Config


logger = Logger(Config.LOGGER_NAME,
                Config.LOG_PATH,
                Config.LOG_NAME)
SPREADSHEET_URL = Config.SPREADSHEET_URL

if __name__ == "__main__":
    logger.debug("START: Spreadsheet URL defined: %s", SPREADSHEET_URL)
    google_spreadsheets.load(SPREADSHEET_URL)

    corgi_counter = Counter()
    keys = google_spreadsheets.keys(include_empty_keys=True)
    for emoji in keys:
        corgis = google_spreadsheets.get_all(emoji)
        corgi_counter[len(corgis)] += 1

    print(tabulate(corgi_counter.items(),
          headers=["# of URLs", "Count"],
          tablefmt="psql"))
