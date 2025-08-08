
import logging
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init
import os

init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }
    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        msg = super().format(record)
        return f"{color}{msg}{Style.RESET_ALL}"

# This will be your shared logger object
logger = logging.getLogger("my_shared_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent double logs

def configure_logger(
    log_file: str = "logs/my_shared_app.log",
    level: int = logging.INFO,
    max_bytes: int = 1_000_000,
    backup_count: int = 5,
):
    """
    Call this ONCE at program start to set up the logger config.
    """
    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = "%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s"
    file_formatter = logging.Formatter(log_format)
    console_formatter = ColorFormatter(log_format)

    # Console (colored)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File (no color)
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)