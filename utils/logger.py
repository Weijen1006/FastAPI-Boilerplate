import logging

class LoggerUtils:
    LOG_FORMAT = '%(asctime)s : %(levelname)s : %(module)s.%(funcName)s : line %(lineno)d : %(message)s'

    @staticmethod
    def get_logger(name = __name__):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(CustomFormatter())

        logger.addHandler(ch)
        logger.propagate = False

        return logger

    @staticmethod
    def set_config():
        logging.basicConfig(level=logging.INFO, format=LoggerUtils.LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = LoggerUtils.LOG_FORMAT

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
logger = LoggerUtils.get_logger(__name__)