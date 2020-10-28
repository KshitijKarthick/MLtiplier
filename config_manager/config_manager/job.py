from dataclasses import dataclass
from typing import AnyStr, Optional, Tuple

JOB_QUEUE_NAME = 'jobs'


@dataclass
class ImageViewerInput:
    target: AnyStr
    source: AnyStr
    target_resolution: Tuple[int, int]
    source_resolution: Tuple[int, int]


@dataclass
class JobStatusState:
    PENDING = 'pending'
    FAILURE = 'failed'
    SUCCESS = 'success'


@dataclass
class JobStatus:
    job_id: int
    status: AnyStr
    error_message: Optional[AnyStr] = None
    queue_length: Optional[int] = None
    payload: Optional[ImageViewerInput] = None


@dataclass
class Job:
    job_id: int
    base_image_resolution: Tuple[int, int]
    increase_resolution_percent: int
    image_dir_name: AnyStr
    high_res_image_name: AnyStr
    retries: int = 0
