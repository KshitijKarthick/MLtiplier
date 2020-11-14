from dataclasses import dataclass
from typing import AnyStr, Optional


@dataclass
class JobStatusState:
    PENDING = "pending"
    FAILURE = "failed"
    SUCCESS = "success"


@dataclass
class MLWorkerInput:
    pass


@dataclass
class MLWorkerResult:
    pass


@dataclass
class HTTPStatusOutput:
    job_id: AnyStr
    status: AnyStr
    result: Optional[MLWorkerResult] = None


@dataclass
class HTTPJobOutput:
    job_id: int
