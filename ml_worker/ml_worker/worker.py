from queue_manager.redis_job_queue import RedisJobQueue
from config_manager.redis import HOST
from config_manager.job import JOB_QUEUE_NAME
from config_manager.utils import get_logger

logger = get_logger()


def job(*_, **__,):
    return 'sample_result'


def main():
    job_queue = RedisJobQueue(host=HOST, queue_name=JOB_QUEUE_NAME,
                              job_fn=job, logger=logger,)
    logger.info('Starting Job queue worker')
    job_queue.run(indefinite_wait=True)


if __name__ == '__main__':
    main()
