import logging
from logging.handlers import RotatingFileHandler
from pathlib import PurePath


def get_logger(logger_name, log_dir_path=None):
    log_dir = PurePath(log_dir_path if log_dir_path else '.')
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_dir / f'{logger_name}.log', maxBytes=2086, backupCount=50)
    logger.addHandler(handler)
    return logger
