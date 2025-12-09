import datetime
import json
from typing import Any, Dict

import gevent
from sqlalchemy import select

from src.core.celery import celery_app
from src.core.database.db import get_sync_session
from src.core.database.models import Task
from src.services.random_number import get_random_numbers


@celery_app.task(name="process_task", queue="celery")
def process_task(task_id: int) -> Dict[str, Any]:
    g = gevent.spawn(get_random_numbers, 1)

    query = select(Task).where(Task.id == task_id)
    with get_sync_session() as session:
        result = session.execute(query)
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"Cannot find task with id {task_id}")
        task.started_at = datetime.datetime.now()
        session.commit()

    result_value: dict = g.get()

    with get_sync_session() as session:
        result = session.execute(query)
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError(f"Cannot find task with id {task_id}")
        task.result = json.dumps(
            {
                "data": result_value.get("data"),
            }
        )
        task.errors = json.dumps(
            {
                "errors": result_value.get("errors")
            }
        )
        task.completed_at = datetime.datetime.now()
        task.status = "COMPLETED"
        session.commit()
        session.refresh(task)
        return {"status": task.status}
