import os
import time
import logging

from backend_server.model import (
    JobPayload, WorkerPayload,
)
from backend_server.utils import get_logger


logger = get_logger(
    logger_name='ml-worker',
    log_dir_path=os.environ.get('LOG_DIR_PATH')
)


def run(job: JobPayload):
    logging.info(f'Running job: {job.json()}')
    time.sleep(15)
    return WorkerPayload(
        data=job.data,
    )
