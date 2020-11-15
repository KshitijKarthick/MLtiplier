from dataclasses import asdict
from typing import AnyStr

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from redis import Redis
from rq import Queue, Retry

from config_manager.commons import (
    DEBUG_MODE,
)
from config_manager.redis import HOST
from config_manager.utils import get_logger

from ml_worker.main import run

from config_manager.schema import (
    JobStatusState,
    HTTPStatusOutput,
    HTTPJobOutput,
    MLWorkerInput,
)

queue = Queue(connection=Redis(HOST))
app = FastAPI()
logger = get_logger()

if DEBUG_MODE:
    app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/api/status")
async def render_status():
    return {"msg": "Ok"}


@app.get("/api/job/status")
async def check_job_status(job_id: AnyStr):
    job_id = job_id.decode("utf-8")
    job = queue.fetch_job(job_id=job_id)
    if not job or job.is_failed:
        raise HTTPException(
            status_code=503,
            detail=f"Fatal error occurred: {job.id}",
        )
    elif not job.is_finished:
        return asdict(HTTPStatusOutput(job_id=job_id, status=JobStatusState.PENDING))
    else:
        return asdict(
            HTTPStatusOutput(
                job_id=job_id, status=JobStatusState.SUCCESS, result=job.result
            )
        )


@app.post("/api/job")
async def anime_image_resize():
    try:
        job = queue.enqueue(
            run,
            MLWorkerInput(),
            retry=Retry(max=3, interval=20),
            result_ttl=60 * 60 * 2,
        )
        return asdict(HTTPJobOutput(job_id=job.id))
    except HTTPException:
        raise
    except BaseException as err:
        logger.exception("Fatal Error")
        raise HTTPException(status_code=503, detail=f"Fatal error occurred: {err}")


logger.info("All application resources are loaded")
