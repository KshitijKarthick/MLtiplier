import os
from fastapi import FastAPI
from redis import Redis
from rq import (
    Queue, Retry,
)

from backend_server import worker
from backend_server.model import (
    JobPayload, JobStatus, JobStatusResponse, JobResponse,
)
from backend_server.utils import get_logger

# Constants from environment vars
LOG_DIR_PATH = os.environ.get('LOG_DIR_PATH')
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME', '0.0.0.0')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

app = FastAPI(
    title="MLtiplier backend server",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
logger = get_logger(
    logger_name='app-server',
    log_dir_path=LOG_DIR_PATH
)
q = Queue(
    connection=Redis(
        host=REDIS_HOSTNAME, port=REDIS_PORT,
    )
)


@app.get("/api/status")
def heartbeat():
    return {"msg": "OK"}


@app.get("/api/status/job/{job_id}")
def job_status(job_id: str) -> JobStatusResponse:
    payload = None
    status = JobStatus.pending
    logger.info(f'Checking job status: {job_id}')
    j = q.fetch_job(job_id=job_id)
    if j.is_finished:
        payload = j.result
        status = JobStatus.completed
    elif j.is_failed:
        status = JobStatus.failed
    return JobStatusResponse(
        job_id=job_id,
        status=status,
        payload=payload,
    )


@app.put("/api/job")
def submit_job(job: JobPayload) -> JobResponse:
    logger.info(f'Submitting a job: {job.json()}')
    j = q.enqueue(
        worker.run, job,
        retry=Retry(max=3, interval=60),
        result_ttl=60 * 10,
        job_timeout=60 * 0.5,
    )
    return JobResponse(
        job_id=j.id,
        job=job,
    )
