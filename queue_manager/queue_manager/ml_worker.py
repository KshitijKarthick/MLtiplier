import json
import logging
import time
from dataclasses import asdict
from typing import AnyStr, Callable, Optional

from redis import Redis, RedisError, ConnectionError
from config_manager.exception import MLPredictionException
from config_manager.schema import (
    Job,
    JobStatus,
    MLWorkerInput,
    JobStatusState,
    MLWorkerResult,
)
from config_manager.redis import HOST
from config_manager.job import JOB_QUEUE_NAME


class MLWorkerQueueManager:
    def __init__(
        self,
        job_fn: Callable,
        host: AnyStr = HOST,
        queue_name: AnyStr = JOB_QUEUE_NAME,
        polling_interval: int = 1,
        job_status_timeout: int = 60 * 60,
        max_retries: int = 3,
        logger: logging.Logger = logging,
    ):
        self.redis = Redis(host)
        self.queue_name = queue_name
        self.job_fn = job_fn
        self.polling_interval = polling_interval
        self.max_retries = max_retries
        self.job_status_timeout = job_status_timeout
        self.logger = logger

    def read_job(self) -> Optional[Job]:
        message = self.redis.lpop(self.queue_name)
        if not message:
            return None
        else:
            parsed_message = json.loads(message.decode("utf-8"))
            print(parsed_message)
            parsed_message["payload"] = MLWorkerInput(**parsed_message["payload"])
            return Job(**parsed_message)

    def insert_job_at_end(self, job: Job) -> int:
        return self.redis.rpush(json.dumps(asdict(job)))

    def insert_job_at_start(self, job: Job) -> int:
        return self.redis.lpush(json.dumps(asdict(job)))

    def set_job_status(self, job_status: JobStatus) -> int:
        return self.redis.setex(
            name=job_status.job_id,
            value=json.dumps(asdict(job_status)),
            time=self.job_status_timeout,
        )

    def run(
        self,
        indefinite_wait: bool = True,
        max_connection_errors: int = 5,
        connection_error_secs: int = 5,
        redis_error_secs: int = 1,
    ) -> None:
        redis_error_count = 0
        while True:
            try:
                job = self.read_job()
                try:
                    if not job:
                        if not indefinite_wait:
                            break
                        else:
                            time.sleep(self.polling_interval)
                            continue
                    self.logger.info(f"Running job: {job.job_id}")
                    ml_worker_result = self.job_fn(job.payload)
                    self.logger.info(f"Job: {job.job_id} completed")
                    job_status = JobStatus(
                        job_id=job.job_id,
                        status=JobStatusState.SUCCESS,
                        result=ml_worker_result,
                        input=job,
                    )
                    self.set_job_status(job_status=job_status)
                except (MLPredictionException, BaseException) as e:
                    if job.retries < self.max_retries:
                        self.logger.exception(
                            f"Exception occurred: retry {job.retries} - {e!s}"
                        )
                        job.retries = job.retries + 1
                        self.insert_job_at_start(job=job)
                    else:
                        error_message = (
                            f"Max number of retry failures. Job: {job.job_id}"
                        )
                        self.logger.exception(error_message)
                        job_status = JobStatus(
                            job_id=job.job_id,
                            status=JobStatusState.FAILURE,
                            input=job,
                            error_message=error_message,
                        )
                        self.set_job_status(job_status=job_status)
            except ConnectionError:
                redis_error_count += 1
                self.logger.exception(f"Redis connection error: {redis_error_count}")
                time.sleep(connection_error_secs)
                if redis_error_count > max_connection_errors:
                    break
            except RedisError as e:
                self.logger.exception(f"Redis exception: {e!s}")
                time.sleep(redis_error_secs)
            except BaseException as e:
                self.logger.exception(f"Fatal Exception: {e!s}")
                raise
