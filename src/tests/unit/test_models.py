from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import Task


@pytest.mark.asyncio
async def test_create_task_defaults(db_session: AsyncSession):
    task = Task(
        name="Test Task",
        description="This is a test task"
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.priority == "LOW"
    assert task.status == "NEW"

    assert task.name == "Test Task"
    assert task.description == "This is a test task"
    assert task.started_at is None
    assert task.completed_at is None
    assert task.result is None
    assert task.errors_occurred is None

@pytest.mark.asyncio
async def test_create_task_full(db_session: AsyncSession):
    now = datetime.utcnow()
    task = Task(
        name="Full Task",
        description="Task with all fields",
        priority="HIGH",
        status="IN_PROGRESS",
        started_at=now,
        completed_at=now,
        result={"output": "ok"},
        errors_occurred={"errors": []}
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.priority == "HIGH"
    assert task.status == "IN_PROGRESS"
    assert task.started_at == now
    assert task.completed_at == now
    assert task.result == {"output": "ok"}
    assert task.errors_occurred == {"errors": []}
