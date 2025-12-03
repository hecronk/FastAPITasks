from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/v1/tasks", tags=["Tasks"])


@router.post("")
async def create_task():
    return

@router.get("")
async def get_tasks():
    return

@router.get("/{task_id}")
async def get_task(task_id: int):
    task = None
    if not task:
        raise HTTPException(status_code=400, detail="Task not found")

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    task = None
    return

@router.get("/{task_id}/status")
async def get_task_status(task_id: int):
    task = None
    return
