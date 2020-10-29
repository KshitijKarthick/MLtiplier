import json
import logging
import time
from dataclasses import asdict

from redis import Redis
from config_manager.schema import Job, JobStatus, MLWorkerPayload, JobStatusState
from config_manager.commons import USER_UPLOAD_PATH, INPUT_IMAGE_NAME


class MLWorkerQueueManager:
    def __init__(self, host, queue_name, job_fn, polling_interval=1,
                 job_status_timeout=60*60, max_retries=3, logger=logging):
        self.redis = Redis(host)
        self.queue_name = queue_name
        self.job_fn = job_fn
        self.polling_interval = polling_interval
        self.max_retries = max_retries
        self.job_status_timeout = job_status_timeout
        self.logger = logger

    def read_job(self):
        message = self.redis.lpop(self.queue_name)
        return Job(**json.loads(message.decode('utf-8'))) if len(message) > 0 else None

    def insert_job_at_end(self, job):
        self.redis.rpush(json.dumps(asdict(job)))

    def insert_job_at_start(self, job):
        self.redis.lpush(json.dumps(asdict(job)))

    def set_job_status(self, job, job_status):
        self.redis.setex(name=job.job_id, value=json.dumps(asdict(job_status)),
                         time=self.job_status_timeout)

    def run(self, indefinite_wait=True):
        while True:
            try:
                job = self.read_job()
                try:
                    if not job:
                        if indefinite_wait:
                            break
                        else:
                            time.sleep(self.polling_interval)
                    self.logger.info(f'Running job: {job.job_id}')
                    high_res_image_resolution = self.job_fn(**asdict(job))
                    self.logger.info(f'Job: {job.job_id} completed')
                    job_status = JobStatus(
                        job_id=job.job_id, status=JobStatusState.SUCCESS,
                        payload=MLWorkerPayload(
                            target=str(USER_UPLOAD_PATH / job.image_dir_name /
                                   job.high_res_image_name),
                            source=str(USER_UPLOAD_PATH / job.image_dir_name / INPUT_IMAGE_NAME),
                            target_resolution=high_res_image_resolution,
                            source_resolution=job.base_image_resolution,
                        )
                    )
                    self.set_job_status(job=job, job_status=job_status)
                except BaseException:
                    if job.retries < self.max_retries:
                        self.logger.exception(f'Exception occurred: retry {job.retries}')
                        job.retries = job.retries + 1
                        self.insert_job_at_start(job=job)
                    else:
                        self.logger.exception(f'Exception occurred retries failed')
                        job_status = JobStatus(job_id=job.job_id, status=JobStatusState.FAILURE,
                                               error_message='Exception occurred retries failed')
                        self.set_job_status(job=job, job_status=job_status)
                        self.set_job_status(job=job, job_status=False)
            except BaseException:
                continue
