from datetime import datetime, timedelta
import uuid
from rest_framework import status

from apps.virtual_education.models import Enrollment
from apps.virtual_education.services.enrollments import EnrollmentService

from apps.virtual_education.tests.factories.enrollments import EnrollmentFactory
from apps.virtual_education.tests.factories.students import StudentFactory, UserFactory
from apps.virtual_education.tests.factories.courses import CourseFactory

from apps.virtual_education.tests.test_main import TestVirtualEducation
from factory.fuzzy import FuzzyChoice


class TestEnrollment(TestVirtualEducation):
    """
    Testes para o modelo Enrollment.
    """

    def setUp(self):
        self.user = UserFactory(nickname='Jaden')
        self.student = StudentFactory(user=self.user)
        self.course = CourseFactory(name="Como ser um duelista de Yu-gi-oh!")
        self.enrollment = EnrollmentFactory(
            student=self.student,
            course=self.course
        )
        self.url = '/enrollments/'

    def test_create_enrollment(self):
        """
        Testa a criação de uma nova matrícula.
        """
        self.enrollment.status = 'Aprovado'
        self.enrollment.save()

        date_close = datetime.now() + timedelta(days=30)
        data = {
            "student": str(self.student.id),
            "course": str(self.course.id),
            "date_close": date_close.strftime('%Y-%m-%d')
        }

        enrollments = Enrollment.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), enrollments + 1)

        new_enrollment = Enrollment.objects.get(
            status='Andamento',
            student=self.student
        )
        self.assertEqual(
            str(new_enrollment.student.id),
            data["student"]
        )
        self.assertEqual(
            str(new_enrollment.course.id),
            data["course"]
        )

    def test_create_enrollment_with_student_enrolled(self):
        """
        Testa a criação de uma matrícula de aluno com uma matrícula em andamento.
        """
        course = CourseFactory()

        date_close = datetime.now() + timedelta(days=30)

        data = {
            "student": str(self.student.id),
            "course": str(course.id),
            "date_close": date_close.strftime('%Y-%m-%d')
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            Enrollment.objects.filter(
                status='Andamento', student=self.student
            ).count(),
            1
        )

    def test_create_enrollment_invalid_student(self):
        """
        Testa a criação de uma nova matrícula com um aluno inválido.
        """
        data = {
            "student": str(uuid.uuid4()),
            "course": str(self.course.id),
            "status": "Aprovado"
        }

        enrollments = Enrollment.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Enrollment.objects.count(), enrollments)
        self.assertEqual(
            str(response.data['student'][0]),
            f'Pk inválido "{data["student"]}" - objeto não existe.'
        )

    def test_create_enrollment_invalid_course(self):
        """
        Testa a criação de uma nova matrícula com um curso inválido.
        """
        data = {
            "student": str(self.student.id),
            "course": str(uuid.uuid4()),
            "status": "Aprovado"
        }

        enrollments = Enrollment.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Enrollment.objects.count(), enrollments)
        self.assertEqual(
            str(response.data['course'][0]),
            f'Pk inválido "{data["course"]}" - objeto não existe.'
        )

    def test_retrieve_enrollment(self):
        """
        Testa a recuperação de uma matrícula existente.
        """
        response = self.client.get(f"{self.url}{self.enrollment.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.enrollment.id))
        self.assertEqual(response.data["student"], self.enrollment.student.id)
        self.assertEqual(response.data["course"], self.enrollment.course.id)
        self.assertEqual(response.data["status"], self.enrollment.status)

    def test_retrieve_enrollment_not_found(self):
        """
        Testa a recuperação de uma matrícula inexistente.
        """
        id = uuid.uuid4()

        response = self.client.get(f"{self.url}{id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Enrollment.objects.filter(id=id))

    def test_list_enrollment(self):
        """
        Testa a listagem de todas as matrículas.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Enrollment.objects.count(), response.data['count'])

    def test_complete_enrollment_aprovado(self):

        # Call the method from EnrollmentService to test
        EnrollmentService.complete_enrollment(
            self.enrollment.student, self.enrollment.course, score=8
        )

        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'Aprovado')
        self.assertTrue(self.enrollment.date_close)

    def test_complete_enrollment_reprovado(self):

        # Call the method from EnrollmentService to test
        EnrollmentService.complete_enrollment(self.enrollment.student, self.enrollment.course, score=5.96)

        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'Reprovado')
        self.assertTrue(self.enrollment.date_close)

    def test_update_enrollment_status(self):
        # A atualização do status de matrícula só é feita pelo score, não diretamente através do endpoint.
        data = {
            "status": "Aprovado"
        }

        response = self.client.patch(f"{self.url}{self.enrollment.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            Enrollment.objects.get(id=self.enrollment.id).status,
            data['status']
        )

    def test_update_enrollment_score(self):
        # Testando a atualização da nota de uma matrícula existente
        data = {
            "score": "9.5"
        }

        response = self.client.patch(f"{self.url}{self.enrollment.id}/", data)

        self.enrollment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.enrollment.score,
            float(data['score'])
        )
        self.assertEqual(
            self.enrollment.status,
            'Aprovado'
        )

    def test_update_enrollment_justification(self):
        # Testando a atualização da justificativa de uma matrícula existente
        data = {
            "justification": "Aluno apresentou motivo pessoal para atraso"
        }

        response = self.client.patch(f"{self.url}{self.enrollment.id}/", data)

        self.enrollment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.enrollment.justification,
            data['justification']
        )
        self.assertEqual(
            self.enrollment.status,
            'Desistiu'
        )

    def test_update_enrollment_data(self):
        # Testando a atualização dos dados de uma matrícula existente

        date_close = datetime.now() + timedelta(days=30)
        student = StudentFactory()
        course = CourseFactory()
        data = {
            "course": course.id,
            "student": student.id,
            "score": "7.2",
            "date_close": date_close.strftime('%Y-%m-%d')
        }

        response = self.client.put(f"{self.url}{self.enrollment.id}/", data)

        self.enrollment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            float(self.enrollment.score),
            float(data['score'])
        )

    def test_filter_enrollments_reprovado(self):
        # Testa a filtragem de enrollments com status 'Reprovado'

        filter_params = {'status': 'Reprovado'}

        EnrollmentFactory.create_batch(
            size=10,
            status=FuzzyChoice(['Aprovado', 'Andamento', 'Desistiu'])
        )

        EnrollmentFactory.create_batch(
            size=5,
            status='Reprovado'
        )

        response = self.client.get(f'{self.url}?status={filter_params["status"]}')

        enrollments_reprovado = Enrollment.objects.filter(
            status__iexact=filter_params['status']
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], enrollments_reprovado)

    def test_filter_enrollments_aprovado(self):
        # Testa a filtragem de enrollments com status 'Aprovado'

        filter_params = {'status': 'Aprovado'}

        EnrollmentFactory.create_batch(
            size=10,
            status=FuzzyChoice(['Reprovado', 'Andamento', 'Desistiu'])
        )

        EnrollmentFactory.create_batch(
            size=5,
            status='Aprovado'
        )

        response = self.client.get(f'{self.url}?status={filter_params["status"]}')

        enrollments_aprovado = Enrollment.objects.filter(
            status__iexact=filter_params['status']
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], enrollments_aprovado)

    def test_filter_enrollments_andamento(self):
        # Testa a filtragem de enrollments com status 'Andamento'

        filter_params = {'status': 'Andamento'}

        EnrollmentFactory.create_batch(
            size=10,
            status=FuzzyChoice(['Reprovado', 'Aprovado', 'Desistiu'])
        )

        EnrollmentFactory.create_batch(
            size=5
        )

        response = self.client.get(f'{self.url}?status={filter_params["status"]}')

        enrollments_andamento = Enrollment.objects.filter(
            status__iexact=filter_params['status']
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], enrollments_andamento)

    def test_filter_enrollments_desistiu(self):
        # Testa a filtragem de enrollments com status 'Desistiu'

        filter_params = {'status': 'Desistiu'}

        EnrollmentFactory.create_batch(
            size=10,
            status=FuzzyChoice(['Reprovado', 'Aprovado', 'Aprovado'])
        )

        EnrollmentFactory.create_batch(
            size=5
        )

        response = self.client.get(f'{self.url}?status={filter_params["status"]}')

        enrollments_desistiu = Enrollment.objects.filter(
            status__iexact=filter_params['status']
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], enrollments_desistiu)

    def test_filter_enrollments_student(self):
        # Testa a filtragem de matrículas de um mesmo 'Student'

        EnrollmentFactory.create_batch(
           size=5,
           student=self.student,
           status=FuzzyChoice(['Aprovado', 'Reprovado'])
        )

        response = self.client.get(f"{self.url}?student={str(self.student.id)}")

        student_enrollments = Enrollment.objects.filter(
            student=self.student
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], student_enrollments)

    def test_filter_enrollments_course(self):
        # Testa a filtragem de matrículas de um mesmo 'Course'

        EnrollmentFactory.create_batch(
           size=15
        )

        EnrollmentFactory.create_batch(
            size=8,
            course=self.course
        )

        filter_params = {'course': self.course.id}

        response = self.client.get(f"{self.url}?course={filter_params['course']}")

        course_enrollments = Enrollment.objects.filter(
            course=filter_params['course']
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], course_enrollments)

    def test_filter_enrollments_date_enroll(self):
        # Testa a filtragem de matrículas criadas a partir de uma data

        self.enrollment.date_enroll = datetime.now() - timedelta(days=90)
        self.enrollment.save()

        date = {'date_enroll': datetime.now() - timedelta(days=7)}
        EnrollmentFactory.create_batch(
           size=15,
           date_enroll=date['date_enroll']
        )

        response = self.client.get(f"{self.url}?date_enroll={date['date_enroll'].date()}")

        date_enrollments = Enrollment.objects.filter(
            date_enroll__gte=date['date_enroll'].date()
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], date_enrollments)

    def test_filter_enrollments_date_closed(self):
        # Testa a filtragem de matrículas encerradas a partir de uma data

        date = {'date_enroll': datetime.now() - timedelta(days=30)}

        self.enrollment.date_enroll = datetime.now() - timedelta(days=90)
        self.enrollment.date_close = datetime.now() - timedelta(days=30)
        self.enrollment.save()

        EnrollmentFactory.create_batch(
           size=5
        )

        response = self.client.get(f"{self.url}?date_enroll={date['date_enroll'].date()}")

        date_enrollments = Enrollment.objects.filter(
            date_enroll__gte=date['date_enroll'].date()
        ).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], date_enrollments)

    def test_apagar_enrollment(self):
        # Testa a filtragem de matrículas encerradas a partir de uma data

        response = self.client.delete(f"{self.url}{self.enrollment.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Enrollment.objects.filter(id=self.enrollment.id))
