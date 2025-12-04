from celery import Celery

from src.core.settings.settings import settings


celery_app = Celery(
    "tasks-worker",
    broker=settings.broker_url,
    backend=settings.result_backend,
)

PRIORITY_MAP = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
}

celery_app.conf.update(
    task_ignore_result=False,
    broker_connection_retry_on_startup=True,
    database_create_tables_at_setup=True,
    database_table_schemas={
        "task": "celery",
        "group": "celery",
    },
    database_table_names={
        "task": "task",
        "group": "group",
    },
    task_queues = {
        "default": {
            "exchange": "default",
            "routing_key": "default",
            "queue_arguments": {"x-max-priority": 3}
        },
        "celery": {
        "exchange": "celery",
        "routing_key": "celery",
        "queue_arguments": {"x-max-priority": 3}
        }
    }
)

celery_app.autodiscover_tasks(["src.tasks"])
