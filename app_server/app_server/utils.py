import logging
import math

from config_manager.config_manager.commons import MAX_ALLOWED_SIZE, LOGS_DIR_PATH


def valid_resolution_size(upscaled_size, max_size=MAX_ALLOWED_SIZE):
    try:
        x, y = upscaled_size
        if isinstance(x, int) and isinstance(y, int) and x <= max_size[0] and y <= \
                max_size[1]:
            return True
        else:
            return False
    except (ValueError, TypeError):
        return False


def obtain_enhanced_size(increase_resolution_percent, base_image_resolution):
    def make_even_num(num):
        return num if num % 2 == 0 else num + 1

    enhanced_size = (
        make_even_num(base_image_resolution[0] + math.ceil(
            increase_resolution_percent * base_image_resolution[0] / 100.0)),
        make_even_num(base_image_resolution[1] + math.ceil(
            increase_resolution_percent * base_image_resolution[1] / 100.0))
    )
    return enhanced_size


def build_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler_fp = logging.FileHandler(LOGS_DIR_PATH / "server.log")
    handler_fp.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler_fp.setFormatter(formatter)
    logger.addHandler(handler_fp)
    return logger
