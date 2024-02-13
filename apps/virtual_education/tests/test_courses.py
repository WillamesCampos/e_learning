import uuid
from rest_framework import status

from apps.virtual_education.models import Course
from apps.virtual_education.tests.factories.courses import CourseFactory
from apps.virtual_education.tests.factories.enrollments import EnrollmentFactory
from apps.virtual_education.tests.factories.students import StudentFactory
from apps.virtual_education.tests.test_main import TestVirtualEducation


class TestCourse(TestVirtualEducation):
    """
    Testes para o modelo Course.
    """

    def setUp(self):
        self.course = CourseFactory(name="Python para Iniciantes")
        self.url = '/courses/'

    def test_create_course(self):
        """
        Testa a criação de um novo curso.
        """
        data = {
            "name": "Como treinar o seu dragão",
            "description": "Aventura épica de amizade entre um jovem viking e seu dragão.",
            "duration": 10
        }

        courses = Course.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), courses + 1)
        self.assertTrue(Course.objects.filter(name=data['name']))

    def test_create_course_without_name(self):
        """
        Testa a criação de um novo curso sem o nome.
        """
        data = {
            "description": "Django - Fundamentos",
            "duration": 10
        }

        courses = Course.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), courses)
        self.assertEqual(
            str(response.data['name'][0]),
            'Este campo é obrigatório.'
        )

    def test_retrieve_course(self):
        """
        Testa a recuperação de um curso existente.
        """
        response = self.client.get(f"{self.url}{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.course.id))
        self.assertEqual(response.data["name"], self.course.name)

    def test_retrieve_course_not_found(self):
        """
        Testa a recuperação de um curso inexistente.
        """
        id = uuid.uuid4()

        response = self.client.get(f"{self.url}{id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Course.objects.filter(id=id))

    def test_list_course(self):
        """
        Testa a listagem de todos os cursos.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.count(), response.data['count'])

    def test_update_course_name(self):
        # Testando a atualização do nome de um curso existente
        data = {
            "name": "Como despertar o Mangekyou Sharingan"
        }

        response = self.client.patch(f"{self.url}{self.course.id}/", data)

        self.course.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.course.name,
            data['name']
        )

    def test_update_course_description_to_blank(self):
        # Testando a atualização da descrição de um curso existente
        data = {
            "description": ""
        }

        response = self.client.patch(f"{self.url}{self.course.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(
            Course.objects.get(id=self.course.id).description,
            data['description']
        )
        self.assertEqual(
            str(response.data['description'][0]),
            'Este campo não pode ser em branco.'
        )

    def test_update_course_description(self):
        # Testando a atualização da descrição de um curso existente
        data = {
            "description": "Lorem Ipsum"
        }

        response = self.client.patch(f"{self.url}{self.course.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Course.objects.get(id=self.course.id).description,
            data['description']
        )

    def test_update_course_data(self):
        # Testando a atualização dos dados de um curso existente
        data = {
            "name": "Python Advanced",
            "description": "Advanced concepts in Python programming",
            "duration": 30
        }

        response = self.client.put(f"{self.url}{self.course.id}/", data)

        self.course.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.course.name,
            data['name']
        )
        self.assertEqual(
            self.course.description,
            data['description']
        )

    def test_delete_course_without_students_enrolled(self):

        course_without_enrollments = CourseFactory()

        response = self.client.delete(f'{self.url}{course_without_enrollments.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=course_without_enrollments.id).exists())

    def test_delete_course_with_students_enrolled(self):

        student = StudentFactory()
        EnrollmentFactory(
            course=self.course,
            student=student,
            status='Andamento'
        )

        response = self.client.delete(f'{self.url}{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            Course.objects.filter(id=self.course.id).exists()
        )
