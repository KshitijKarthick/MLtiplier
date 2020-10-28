import json
from config_manager.config_manager.job import JOB_QUEUE_NAME, Job, JobStatus, JobStatusState
from config_manager.config_manager.redis import HOST
from dataclasses import asdict
from uuid import uuid4
from redis import Redis


class RedisJobProducer:
    def __init__(self, host=HOST, job_queue_name=JOB_QUEUE_NAME):
        self.redis = Redis(host)
        self.job_queue_name = job_queue_name
        self.job_queue_ids_name = f'{job_queue_name}_ids'

    def submit(self, payload):
        job_id = uuid4().hex
        job = Job(**{'job_id': job_id, **payload})
        self.redis.rpush(self.job_queue_name, self._marshall(asdict(job)))
        self.redis.rpush(self.job_queue_ids_name, job_id)
        return job_id

    @staticmethod
    def _unmarshall(value):
        return json.loads(value.decode('utf-8')) if value else None

    @staticmethod
    def _marshall(value):
        return json.dumps(value)

    def status(self, job_id):
        # queue_length = self.redis.lindex(name=self.job_queue_ids_name, index=job_id)
        queue_length = 0
        job_status_dict = self._unmarshall(self.redis.get(job_id))
        if job_status_dict:
            job_status = JobStatus(**job_status_dict)
            job_status.queue_length = queue_length
        else:
            job_status = JobStatus(job_id=job_id, status=JobStatusState.PENDING,
                                   queue_length=queue_length)
        return job_status
