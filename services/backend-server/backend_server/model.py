from typing import Optional
from pydantic import BaseModel
from enum import Enum


class JobStatus(str, Enum):
    failed = "FAILED"
    pending = "PENDING"
    completed = "COMPLETED"


class JobPayload(BaseModel):
    """Request sent from user while submitting job."""
    data: Optional[str]


class WorkerPayload(BaseModel):
    """ML Worker response for a specific job."""
    data: Optional[str]


class JobStatusResponse(BaseModel):
    """Response for the API which checks the status of a Job."""
    job_id: str
    status: JobStatus
    payload: Optional[WorkerPayload]


class JobResponse(BaseModel):
    """Response for the API after submitting a job."""
    job_id: str
    job: JobPayload
