import faker
from rest_framework.test import APIClient, APITestCase


class TestVirtualEducation(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.fake = faker.Faker('pt_BR')
        cls.client = APIClient()
        return super().setUpTestData()
