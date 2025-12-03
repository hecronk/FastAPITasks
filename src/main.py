import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from fastapi import FastAPI

from src.core.database.db import AsyncSessionLocal
from src.routers.v1.tasks import router as v1_tasks_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.loop = asyncio.get_running_loop()
    app.state.async_session = AsyncSessionLocal
    app.state.thread_pool = ThreadPoolExecutor(max_workers=10)
    app.state.process_pool = ProcessPoolExecutor(max_workers=4)

@app.on_event("shutdown")
async def shutdown_event():
    app.state.thread_pool.shutdown(wait=True)
    app.state.process_pool.shutdown(wait=True)

app.include_router(v1_tasks_router)
