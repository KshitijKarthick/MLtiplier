from dataclasses import asdict
from typing import AnyStr

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from queue_manager.redis_job_producer import RedisJobProducer
from config_manager.commons import USER_UPLOAD_PATH, MAX_ALLOWED_SIZE, DEBUG_MODE, \
    HIGH_RES_IMAGE_NAME, INPUT_IMAGE_NAME
from config_manager.utils import get_logger

from config_manager.job import JobStatusState

app = FastAPI()
redis_job_manager = RedisJobProducer()
logger = get_logger()

if DEBUG_MODE:
    app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/api/status")
async def render_status():
    return {"msg": "Ok"}


@app.get("/api/job/status/{job_id}")
async def check_job_status(job_id: AnyStr):
    job_status = redis_job_manager.status(job_id=job_id)
    if job_status.status == JobStatusState.FAILURE:
        raise HTTPException(status_code=503, detail=f'Fatal error occurred: '
                                                    f'{job_status.error_message}')
    return asdict(job_status)


@app.post("/api/job")
async def anime_image_resize():
    try:
        job_id = redis_job_manager.submit({})
        return {
            'job_id': job_id
        }
    except HTTPException:
        raise
    except BaseException as err:
        logger.exception('Fatal Error')
        raise HTTPException(status_code=503, detail=f'Fatal error occurred: {err}')


logger.info("All application resources are loaded")
