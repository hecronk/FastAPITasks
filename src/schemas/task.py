from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from src.schemas.common import BaseSchema


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Status(str, Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TaskSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    priority: Priority
    status: Status
    started_at: datetime | None
    completed_at: datetime | None
    result: str | None
    errors_occurred: list[str] | None


class CreateTaskSchema(BaseModel):
    name: str
    description: str
    priority: Priority
