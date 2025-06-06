import os

from celery import Celery
from celery.schedules import crontab
from .tasks import update_null_states

broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery = Celery("app", broker=broker_url, backend=broker_url)


celery.conf.task_routes = {
    "tasks.*": {"queue": "default"},
}

celery.conf.beat_schedule = {
    "update-trackers-every-minute": {
        "task": "tasks.update_null_states",
        "schedule": crontab(minute="*"),  # каждую минуту
    },
}

