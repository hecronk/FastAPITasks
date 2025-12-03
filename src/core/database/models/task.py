import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from src.core.database.db import Base
from src.core.database.models.common import BaseModel


class Task(BaseModel, Base):

    __tablename__ = "tasks"

    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    priority = sa.Column("priority_type", ENUM("LOW", "MEDIUM", "HIGH", name="priority_type"), nullable=False)
    status = sa.Column("task_status", ENUM("NEW", "PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED", name="task_status"), nullable=False)
    started_at = sa.Column(sa.DateTime)
    completed_at = sa.Column(sa.DateTime)
    result = sa.Column(sa.JSON)
    errors_occurred = sa.Column(sa.JSON)
