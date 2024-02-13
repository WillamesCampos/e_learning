import faker
from factory import lazy_attribute
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyText
from apps.virtual_education.models import Course


fake = faker.Faker('pt_BR')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    name = lazy_attribute(lambda obj: fake.job())
    description = FuzzyText(length=200)
    holder_image = Faker('image_url')
    duration = Faker('random_int', min=1, max=10)
