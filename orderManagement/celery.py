import os
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orderManagement.settings')

app = Celery('orderManagement')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# The default scheduler (storing the schedule in the celerybeat-schedule file)
# log delivery boy details every 5 minute
# To Execute daily at midnight. use crontab(minute=0, hour=0)
app.conf.beat_schedule = {
    'add-every-5-minutes': {
        'task': 'orderManagement.core.task.logDboyDetails',
        'schedule': crontab(minute='*/5'),
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()



# CELERY START CMD
# celery -A orderManagement worker -B --concurrency=1 ---loglevel=info
# -B to use celery beats feature
# --concurrency=1 to use only one worker
