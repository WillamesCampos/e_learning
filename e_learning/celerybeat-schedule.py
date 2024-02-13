from e_learning.celery import app
from celery.schedules import crontab


app.conf.beat_schedule = {
    'notify_enrollments_near_to_expire': {
        'task': 'apps.virtual_education.tasks.notify_enrollments_near_to_expire',
        'schedule': crontab(hour=8, minute=0)
    }
}
