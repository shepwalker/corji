import corji.cache as cache
import corji.data_sources as data_sources
from corji.logging import Logger
from corji.settings import Config


logger = Logger(Config.LOGGER_NAME,
                Config.LOG_PATH,
                Config.LOG_NAME)
SPREADSHEET_URL = Config.SPREADSHEET_URL
logger.debug("START: Spreadsheet URL defined: %s", SPREADSHEET_URL)
corgis = data_sources.load_from_spreadsheet(SPREADSHEET_URL)


if __name__ == "__main__":
    logger.debug("START: Starting to load Corjis into cache.")
    cache.put_in_remote_cache(corgis)
    logger.debug("START: Completed Corji Cache loading")
