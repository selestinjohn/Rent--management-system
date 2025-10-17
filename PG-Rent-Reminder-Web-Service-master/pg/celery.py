import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pg.settings')

app = Celery('pg')

# Load configuration from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in all installed apps
app.autodiscover_tasks()

# Define periodic task schedule
app.conf.beat_schedule = {
    'check-due-dates-every-minute': {
        'task': 'sms.tasks.check_due_dates_and_send_sms',
        'schedule': crontab(minute='*'),  # every 1 minute
    },
}

# Optional: set timezone (optional but good for clarity)
app.conf.timezone = 'Africa/Dar_es_Salaam'
