from queue_manager.ml_worker import MLWorkerQueueManager
from config_manager.utils import get_logger
from config_manager.schema import MLWorkerResult, MLWorkerInput

logger = get_logger()


def job(params: MLWorkerInput) -> MLWorkerResult:
    return MLWorkerResult()


def main():
    job_queue = MLWorkerQueueManager(
        job_fn=job,
        logger=logger,
    )
    logger.info("Starting Job queue worker")
    job_queue.run(indefinite_wait=True)


if __name__ == "__main__":
    main()
