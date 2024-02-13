from datetime import datetime, timedelta
from apps.virtual_education.models import Enrollment
from .services.enrollments import EnrollmentService
from e_learning.celery import app


@app.task
def notify_enrollments_near_to_expire():

    enrollments_expiring = Enrollment.objects.filter(
        date_close__lt=datetime.now() + timedelta(days=7),
        status='Andamento'
    )

    for enrollment in enrollments_expiring:
        EnrollmentService.notify_students_of_enrollment(enrollment)
