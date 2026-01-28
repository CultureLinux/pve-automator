import logging
from logging.handlers import RotatingFileHandler
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "pve-automator.log"

LOG_DIR.mkdir(exist_ok=True)

def setup_logging(level=logging.INFO):
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] "
        "%(name)s "
        "%(message)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[file_handler, console_handler],
    )
