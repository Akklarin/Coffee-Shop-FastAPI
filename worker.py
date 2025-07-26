from celery import Celery

celery_app = Celery(
    "my_project",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["src.tasks.celery_tasks"],
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

celery_app.conf.beat_schedule = {
    "delete-unverified_everyday": {
        "task": "delete_unverified_users",
        "schedule": 60 * 60 * 24,
    },
}
