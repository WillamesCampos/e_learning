from datetime import datetime, timedelta
from factory.django import DjangoModelFactory
from factory import lazy_attribute, SubFactory
from factory.fuzzy import FuzzyChoice

from apps.virtual_education.models import Enrollment
from apps.virtual_education.tests.factories.courses import CourseFactory
from apps.virtual_education.tests.factories.students import StudentFactory


class EnrollmentFactory(DjangoModelFactory):
    class Meta:
        model = Enrollment

    student = SubFactory(StudentFactory)
    course = SubFactory(CourseFactory)
    score = FuzzyChoice([number for number in range(0, 11)])
    date_close = datetime.now() + timedelta(days=30)
