import logging

from config_manager.commons import LOGS_DIR_PATH


def get_logger(log_file_name="server.log"):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler_fp = logging.FileHandler(LOGS_DIR_PATH / log_file_name)
    handler_fp.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler_fp.setFormatter(formatter)
    logger.addHandler(handler_fp)
    logger.addHandler(logging.StreamHandler())
    return logger
