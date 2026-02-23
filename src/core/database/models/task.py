import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from typing import Optional, Any
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.db import Base
from src.core.database.models.common import BaseModel


class Task(BaseModel, Base):

    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(sa.String(), nullable=False)
    description: Mapped[str] = mapped_column(sa.String(), nullable=False)
    priority: Mapped[str] = mapped_column(ENUM("LOW", "MEDIUM", "HIGH", name="priority_type"), default="LOW", nullable=False)
    status: Mapped[str] = mapped_column(ENUM("NEW", "PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED", name="task_status"), default="NEW", nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(sa.DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(sa.DateTime)
    result: Mapped[Optional[Any]] = mapped_column(sa.JSON)
    errors_occurred: Mapped[Optional[Any]] = mapped_column(sa.JSON)
