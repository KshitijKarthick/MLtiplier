import os
import tempfile
from dataclasses import asdict
from typing import AnyStr

from PIL import Image

from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pathlib import PosixPath

from redis_job_producer import RedisJobProducer
from config_manager.config_manager.commons import USER_UPLOAD_PATH, MAX_ALLOWED_SIZE, DEBUG_MODE, \
    HIGH_RES_IMAGE_NAME, INPUT_IMAGE_NAME
from utils import build_logger, valid_resolution_size, obtain_enhanced_size

from config_manager.config_manager.job import JobStatusState

app = FastAPI()
redis_job_manager = RedisJobProducer()
logger = build_logger()

if DEBUG_MODE:
    app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get("/api/status")
async def render_status():
    return {"msg": "Ok"}


@app.get("/api/anime/status/{job_id}")
async def check_job_status(job_id: AnyStr):
    job_status = redis_job_manager.status(job_id=job_id)
    if job_status.status == JobStatusState.FAILURE:
        raise HTTPException(status_code=503, detail=f'Fatal error occurred: '
                                                    f'{job_status.error_message}')
    return asdict(job_status)


@app.post("/api/anime/job")
async def anime_image_resize(file: UploadFile = File(...),
                             increase_resolution_percent: int = 100):
    try:
        temp_dir_path = PosixPath(tempfile.mkdtemp(dir=USER_UPLOAD_PATH))
        temp_dir_name = str(temp_dir_path.parts[-1])
        high_res_image_name = HIGH_RES_IMAGE_NAME
        input_image_path = (temp_dir_path / INPUT_IMAGE_NAME)
        _, extension = os.path.splitext(file.filename)
        binary_img_content = await file.read()

        # Expected img bytes to be uploaded
        if not len(binary_img_content) > 0:
            raise HTTPException(status_code=412, detail="Invalid image uploaded, no bytes "
                                                        "obtained for the image")

        img = Image.open(BytesIO(binary_img_content)).convert("RGB")
        base_image_resolution = (img.height, img.width)
        enhanced_img_size = obtain_enhanced_size(
            increase_resolution_percent=increase_resolution_percent,
            base_image_resolution=base_image_resolution)

        # Disallow very large images to be predicted for memory constraints
        if not valid_resolution_size(upscaled_size=enhanced_img_size):
            raise HTTPException(status_code=413,
                                detail=f"Very high resolution expected, "
                                       f"max allowed resolution {MAX_ALLOWED_SIZE}")

        img.save(input_image_path, "JPEG")
        job_id = redis_job_manager.submit({
            'base_image_resolution': base_image_resolution,
            'increase_resolution_percent': increase_resolution_percent,
            'image_dir_name': temp_dir_name,
            'high_res_image_name': high_res_image_name,
        })
        del(img, file, binary_img_content)
        return {
            'job_id': job_id
        }
    except HTTPException:
        raise
    except BaseException as err:
        logger.exception('Fatal Error')
        raise HTTPException(status_code=503, detail=f'Fatal error occurred: {err}')


logger.info("All application resources are loaded")
