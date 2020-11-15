from config_manager.utils import get_logger


logger = get_logger(log_file_name="worker.log")
logger.info("Starting Python RQ worker")


def run(ml_worker_input):
    logger.info(f"Received job: {ml_worker_input}")
    return "Hello World"
