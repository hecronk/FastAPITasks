from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.celery import PRIORITY_MAP
from src.core.database.db import get_session
from src.core.database.models import Task
from src.dependencies.pagination import get_pagination
from src.schemas.task import CreateTaskSchema, TaskSchema
from src.tasks.tasks import process_task

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.post("", response_model=TaskSchema)
async def create_task(create_task_schema: CreateTaskSchema, session: AsyncSession = Depends(get_session)):
    try:
        created_task = Task(
            name=create_task_schema.name,
            description=create_task_schema.description,
            priority=create_task_schema.priority.value,
        )
        session.add(created_task)
        await session.commit()
        await session.refresh(created_task)
        process_task.apply_async(args=[created_task.id,], priority=PRIORITY_MAP[created_task.priority])
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return created_task

@router.get("", response_model=List[TaskSchema])
async def get_tasks(pagination: dict = Depends(get_pagination), session: AsyncSession = Depends(get_session)):
    offset = (pagination["page"] - 1) * pagination["page_size"]
    query = select(Task).offset(offset).limit(pagination["page_size"])
    result = await session.execute(query)
    tasks = result.scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Task).where(Task.id==task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "CANCELLED"
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return {"status": task.status}

@router.get("/{task_id}/status")
async def get_task_status(task_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": task.status}
