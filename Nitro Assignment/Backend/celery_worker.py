# backend/app/celery_worker.py

from celery import Celery
import os

# Celery broker and backend URLs (read from environment or docker-compose)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery(
    "file_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

# Import custom celery config if any (optional)
celery_app.config_from_object("app.celeryconfig", silent=True)

# Autodiscover tasks in tasks.py of app package
celery_app.autodiscover_tasks(['app'])

if __name__ == "__main__":
    celery_app.start()
