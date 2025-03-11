import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('config')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.task_acks_late = True
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.broker_transport_options = {'visibility_timeout': 3600}

celery_app.conf.beat_schedule = {
    'clean_old_trades_every_2_weeks': {
        'task': 'trading.tasks.clean_old_trades',
        'schedule': crontab(day_of_month='1,15', hour=0, minute=0),
    },
}
