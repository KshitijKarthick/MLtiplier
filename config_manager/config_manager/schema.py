from dataclasses import dataclass
from typing import AnyStr, Optional, Tuple


@dataclass
class JobStatusState:
    PENDING = 'pending'
    FAILURE = 'failed'
    SUCCESS = 'success'


@dataclass
class MLWorkerInput:
    pass


@dataclass
class MLWorkerResult:
    pass


@dataclass
class JobStatus:
    job_id: int
    status: AnyStr
    error_message: Optional[AnyStr] = None
    queue_length: Optional[int] = None
    input: Optional[MLWorkerInput] = None
    result: Optional[MLWorkerResult] = None


@dataclass
class Job:
    job_id: int
    payload: Optional[MLWorkerInput] = None
    retries: int = 0


@dataclass
class HTTPStatusOutput:
    job_id: int
    status: AnyStr
    result: Optional[MLWorkerResult] = None


@dataclass
class HTTPJobOutput:
    job_id: int
