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

# TODO: Make this shit multithreaded.  It takes too long.
# TODO: Better sysout. ("20% (9/180) complete, that kind of thing.")
if __name__ == "__main__":
    logger.debug("START: Starting to load Corjis into cache.")
    logger.debug("START: Spreadsheet URL defined: %s", SPREADSHEET_URL)
    google_spreadsheets.load(SPREADSHEET_URL)
    s3.load()
    s3.put_all(google_spreadsheets.corgis)
    logger.debug("START: Completed Corji Cache loading")
