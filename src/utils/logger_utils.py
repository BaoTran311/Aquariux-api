import logging

from colorama import Fore, Style

from src.consts import PYTHON_CONFIG

logger = logging.getLogger(PYTHON_CONFIG)
LOG_COLOR = {
    logging.DEBUG: Fore.LIGHTBLACK_EX,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLOR.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"


def setup_logging(
        log_level=logging.INFO,
) -> None:
    log_format = '%(asctime)s | %(levelname)s | %(message)s'
    date_format = "%d-%m-%Y %H:%M:%S"

    # Remove existing handlers to prevent duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(log_level)

    # Console handler
    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    formatter = ColoredFormatter(log_format, datefmt=date_format)
    stream.setFormatter(formatter)
    logger.addHandler(stream)
