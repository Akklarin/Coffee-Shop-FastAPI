from celery import Celery

celery_app = Celery(
    "my_project",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["src.tasks.celery_tasks"],
)

celery_app.conf.beat_schedule = {
    "delete-unverified-everyday": {
        "task": "delete_unverified_users",
        "schedule": 60 * 60 * 24,
    },
}

celery_app.conf.timezone = "UTC"
