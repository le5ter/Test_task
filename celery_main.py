from celery.schedules import crontab

from config import Config
from app import create_app


app = create_app()
celery_worker = app.extensions["celery"]

celery_worker.conf.broker_url = Config.CELERY_BROKER_URL
celery_worker.conf.result_backend = Config.CELERY_RESULT_BACKEND
celery_worker.conf.timezone = "Europe/Moscow"
celery_worker.conf.broker_connection_retry_on_startup = True

celery_worker.conf.beat_schedule = {
    'check_transactions': {
        'task': 'app.tasks.check_transaction_status',
        'schedule': crontab(minute='*/5')
    }
}

celery_worker.autodiscover_tasks(
    ['app'],
    force=True
)
