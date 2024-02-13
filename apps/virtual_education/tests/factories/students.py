import faker
from factory.django import DjangoModelFactory
from factory import SubFactory, lazy_attribute
from factory.faker import Faker

from apps.virtual_education.models import Student, User


fake = faker.Faker('pt_BR')


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    nickname = lazy_attribute(lambda obj: fake.first_name())
    email = lazy_attribute(lambda obj: fake.email())
    phone = lazy_attribute(lambda obj: fake.phone_number())


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    user = SubFactory(UserFactory)
    avatar = Faker('image_url')
