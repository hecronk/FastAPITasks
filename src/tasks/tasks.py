from typing import Any, Dict

from sqlalchemy import select

from src.core.celery import celery_app
from src.core.database.db import get_sync_session
from src.core.database.models import Task


@celery_app.task(name="process_task", queue="celery")
def process_task(task_id: int) -> Dict[str, Any]:
    with get_sync_session() as session:
        query = select(Task).where(Task.id == task_id)
        result = session.execute(query)
        task = result.scalar_one_or_none()
        if not task:
            task.status = "FAILED"
        task.status = "COMPLETED"
        session.commit()
        session.refresh(task)
        return {"status": task.status}
