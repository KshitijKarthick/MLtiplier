import logging

from fastapi import FastAPI

from redis import Redis
from rq import (
    Queue, Retry,
)

from backend_server.model import (
    JobPayload, JobStatus, JobStatusResponse, JobResponse,
)
from backend_server import worker


app = FastAPI(
    title="MLtiplier backend server",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
q = Queue(connection=Redis(host='0.0.0.0'))


@app.get("/api/status")
def heartbeat():
    return {"msg": "OK"}


@app.get("/api/status/job/{job_id}")
async def job_status(job_id: str) -> JobStatusResponse:
    payload = None
    status = JobStatus.pending
    logging.info(f'Checking job status: {job_id}')
    j = await q.fetch_job(job_id=job_id)
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
async def submit_job(job: JobPayload) -> JobResponse:
    logging.info(f'Submitting a job: {job.json()}')
    j = await q.enqueue(
        worker.run, job,
        retry=Retry(max=3, interval=60),
        result_ttl=60 * 10,
        job_timeout=60 * 0.5,
    )
    return JobResponse(
        job_id=j.id,
        job=job,
    )
