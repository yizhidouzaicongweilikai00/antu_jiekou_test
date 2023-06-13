import logging
from logging.handlers import TimedRotatingFileHandler

from common.utils import Utils

__LOGGER = None


def get_logger():
    global __LOGGER
    if __LOGGER is None:
        __LOGGER = logging.getLogger('byterunner')
        __LOGGER.handlers.clear()
        __LOGGER.setLevel(logging.INFO)

        file_name = Utils.get_project_dir() + "/byterunner.log"
        file_handler = TimedRotatingFileHandler(filename=file_name, when="D", interval=1, backupCount=3)
        file_handler.setLevel(logging.INFO)

        format_str = "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
        date_format_str = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(format_str, date_format_str)
        file_handler.setFormatter(formatter)

        __LOGGER.addHandler(file_handler)
    return __LOGGER
