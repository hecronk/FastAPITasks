from fastapi import FastAPI

from src.routers.v1.tasks import router as v1_tasks_router

app = FastAPI()

app.include_router(v1_tasks_router)
