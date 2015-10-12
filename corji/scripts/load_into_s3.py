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
logger.debug("START: Spreadsheet URL defined: %s", SPREADSHEET_URL)
corgis = google_spreadsheets.get_all(SPREADSHEET_URL)


if __name__ == "__main__":
    logger.debug("START: Starting to load Corjis into cache.")
    s3.put_all(corgis)
    logger.debug("START: Completed Corji Cache loading")
