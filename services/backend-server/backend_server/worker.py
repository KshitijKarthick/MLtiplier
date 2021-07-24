import time
import logging

from backend_server.model import (
    JobPayload, WorkerPayload,
)


def run(job: JobPayload):
    logging.info(f'Running job: {job.json()}')
    time.sleep(15)
    return WorkerPayload(
        data=job.data,
    )
