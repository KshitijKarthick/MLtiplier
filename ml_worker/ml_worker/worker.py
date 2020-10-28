import os
from resizer import predict_with_custom_resizing, build_learner
from redis_job_queue import RedisJobQueue
from config_manager.config_manager.redis import HOST
from config_manager.config_manager.commons import USER_UPLOAD_PATH
from config_manager.config_manager.job import JOB_QUEUE_NAME
from utils import get_logger

learner = build_learner()
logger = get_logger()


def job(base_image_resolution, increase_resolution_percent, image_dir_name, high_res_image_name,
        *_, **__,):
    image_dir_path = USER_UPLOAD_PATH / image_dir_name
    high_res_image_path = image_dir_path / high_res_image_name
    high_res_image = predict_with_custom_resizing(
        learner=learner, image_dir_path=image_dir_path,
        base_image_resolution=base_image_resolution,
        increase_resolution_percent=increase_resolution_percent,
    )
    high_res_image_resolution = list(high_res_image.shape)
    high_res_image.save(high_res_image_path)
    os.system(f'chmod -R 775 {str(image_dir_path)}')
    del high_res_image
    return high_res_image_resolution


def main():
    job_queue = RedisJobQueue(host=HOST, queue_name=JOB_QUEUE_NAME,
                              job_fn=job, logger=logger,)
    logger.info('Starting Job queue worker')
    job_queue.run(indefinite_wait=True)


if __name__ == '__main__':
    main()
