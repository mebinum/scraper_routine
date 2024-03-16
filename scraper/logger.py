import logging

logging.basicConfig(level=logging.INFO, format="%(funcName)s: %(message)s")
Logger = logging.getLogger(__name__)
def log(message):
    Logger.info(message)
