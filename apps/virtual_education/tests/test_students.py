from datetime import datetime, timedelta
import uuid
from rest_framework import status
from apps.virtual_education.filters.students import StudentFilter

from apps.virtual_education.models import Enrollment, Student, User
from apps.virtual_education.tests.factories.enrollments import EnrollmentFactory
from apps.virtual_education.tests.factories.students import StudentFactory, UserFactory
from apps.virtual_education.tests.factories.courses import CourseFactory
from apps.virtual_education.tests.test_main import TestVirtualEducation


class TestStudent(TestVirtualEducation):
    def setUp(self):
        self.user = UserFactory(nickname="Tanjiro")
        self.student = StudentFactory(user=self.user)
        self.url = '/students/'

    def test_create_student(self):
        """
        Testa a criação de um novo aluno.
        Verifica se o aluno é criado com sucesso no banco de dados.
        """
        data = {
            "nickname": "Tomioka",
            "phone": self.fake.phone_number(),
            "email": self.fake.email()
        }

        students = Student.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), students + 1)
        self.assertTrue(Student.objects.filter(user__nickname=data["nickname"]))

    def test_create_student_without_nickname(self):
        """
        Testa a criação de um novo aluno sem o campo nickname.
        Verifica se a requisição retorna o status HTTP 400 (Bad Request)
        e se o campo de apelido é obrigatório.
        """
        data = {
            "phone": self.fake.phone_number(),
            "email": self.fake.email()
        }

        students = Student.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Student.objects.count(), students)
        self.assertEqual(
            str(response.data['nickname'][0]),
            'Este campo é obrigatório.'
        )

    def test_create_student_without_email(self):
        """
        Testa a criação de um novo aluno sem o campo de email.
        Verifica se a requisição retorna o status HTTP 400 (Bad Request)
        e se o campo de email é obrigatório.
        """
        data = {
            "nickname": "Muichiro",
            "phone": self.fake.phone_number(),
        }

        students = Student.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Student.objects.count(), students)
        self.assertEqual(
            str(response.data['email'][0]),
            'Este campo é obrigatório.'
        )

    def test_create_student_without_phone(self):
        """
        Testa a criação de um novo aluno sem o campo de telefone (phone).
        Verifica se a requisição retorna o status HTTP 400 (Bad Request)
        e se o campo de telefone é obrigatório.
        """
        data = {
            "nickname": "Tomioka",
            "email": self.fake.email()
        }
        students = Student.objects.count()

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Student.objects.count(), students)
        self.assertEqual(
            str(response.data['phone'][0]),
            'Este campo é obrigatório.'
        )

    def test_retrieve_student(self):
        """
        Testa a recuperação de um aluno existente.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se os dados do aluno estão corretos.
        """
        response = self.client.get(f"{self.url}{self.student.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.student.id)
        self.assertEqual(response.data["nickname"], self.student.user.nickname)

    def test_retrieve_student_not_found(self):
        """
        Testa a recuperação de um aluno inexistente.
        Verifica se a requisição retorna o status HTTP 404 (Not Found)
        e se o aluno não existe no banco de dados.
        """
        id = uuid.uuid4()
        # Testando a recuperação de um aluno existente
        response = self.client.get(f"{self.url}{id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Student.objects.filter(id=id))

    def test_list_student(self):
        """
        Testa a listagem de todos os alunos.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se a quantidade de alunos retornados está correta.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.count(), response.data['count'])

    def test_update_student_nickname(self):
        """
        Testa a atualização do apelido (nickname) de um aluno existente.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se o apelido do aluno foi atualizado corretamente no banco de dados.
        """
        data = {
            "nickname": "Mokuba"
        }

        response = self.client.patch(f"{self.url}{self.student.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()
        self.assertEqual(
            self.student.user.nickname,
            data['nickname']
        )

    def test_update_student_email(self):
        """
        Testa a atualização do email de um aluno existente.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se o email do aluno foi atualizado corretamente no banco de dados.
        """
        data = {
            "email": self.fake.email()
        }

        response = self.client.patch(f"{self.url}{self.student.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()
        self.assertEqual(
            self.student.user.email,
            data['email']
        )

    def test_update_student_phone(self):
        """
        Testa a atualização do telefone (phone) de um aluno existente.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se o telefone do aluno foi atualizado corretamente no banco de dados.
        """
        data = {
            "phone": self.fake.phone_number()
        }

        response = self.client.patch(f"{self.url}{self.student.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()
        self.assertEqual(
            self.student.user.phone,
            data['phone']
        )

    def test_update_student_data(self):
        """
        Testa a atualização dos dados completos de um aluno existente.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se os dados do aluno foram atualizados corretamente no banco de dados.
        """
        data = {
            "nickname": "Kokushibo",
            "phone": self.fake.phone_number(),
            "email": self.fake.email()
        }

        response = self.client.put(f"{self.url}{self.student.id}/", data)

        self.student.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.student.user.email,
            data['email']
        )
        self.assertEqual(
            self.student.user.nickname,
            data['nickname']
        )
        self.assertEqual(
            self.student.user.phone,
            data['phone']
        )

    def test_delete_student_without_enrollment(self):
        """
        Testa a exclusão de um aluno que não possui matrículas.
        Verifica se a requisição retorna o status HTTP 204 (No Content)
        e se o aluno foi removido corretamente do banco de dados.
        """
        response = self.client.delete(f"{self.url}{self.student.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())

    def test_delete_student_with_enrollment(self):
        """
        Testa a exclusão de um aluno que possui matrículas.
        Verifica se a requisição retorna o status HTTP 400 (Bad Request)
        e se o aluno não foi removido do banco de dados.
        Verifica também se a mensagem de erro informa que o aluno está matriculado em um curso.
        """

        course = CourseFactory()
        EnrollmentFactory(
            student=self.student, course=course
        )

        response = self.client.delete(f"{self.url}{self.student.id}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            Student.objects.filter(id=self.student.id).exists()
        )
        self.assertTrue(
            Enrollment.objects.filter(
                student=self.student, course=course
            ).exists()
        )
        self.assertTrue(
            response.data,
            'O aluno está matriculado em um curso. Impossível apagar.'
        )

    def test_date_created_filter(self):
        """
        Testa o filtro de alunos por data de criação.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se a quantidade de alunos retornados está correta.
        """
        filter_date = datetime.now() - timedelta(days=1)
        filter_params = {'date_created': filter_date.strftime('%Y-%m-%d')}
        response = self.client.get(f'{self.url}?date_created={filter_params["date_created"]}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_students = Student.objects.filter(
            user__date_created__gte=filter_params['date_created']
        ).count()
        self.assertEqual(response.data['count'], filtered_students)

    def test_nickname_filter(self):
        """
        Testa o filtro de alunos por apelido (nickname).
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se a quantidade de alunos retornados está correta.
        Verifica também se todos os alunos retornados possuem o apelido filtrado.
        """
        filter_params = {'nickname': 'José'}

        users_nicknames = [
            'José Paulo',
            'José Paes',
            'José',
            'Joseph Paul',
            'Josephe'
        ]

        students = StudentFactory.create_batch(
            size=5
        )

        student_with_new_users = []
        for nickname, student in zip(users_nicknames, students):
            student.user.nickname = nickname
            student_with_new_users.append(student.user)

        User.objects.bulk_update(student_with_new_users, ['nickname'])

        students_nickname_filtered = Student.objects.filter(
            user__nickname__contains=filter_params['nickname']
        ).count()

        response = self.client.get(f'{self.url}?nickname={filter_params["nickname"]}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], students_nickname_filtered)

        for student in response.data['results']:
            self.assertIn(filter_params['nickname'], student['nickname'])

    def test_email_filter(self):
        """
        Testa o filtro de alunos por email.
        Verifica se a requisição retorna o status HTTP 200 (OK)
        e se a quantidade de alunos retornados está correta.
        Verifica também se todos os alunos retornados possuem o email filtrado.
        """

        filter_params = {'email': '@gmail.com'}

        emails = [
            'aluno1@gmail.com',
            'aluno2@gmail.com',
            'aluno3@hotmail.com',
            'aluno4@gmrail.com',
            'aluno5@gmail.com'
        ]

        students = StudentFactory.create_batch(
            size=5
        )

        students_updated = []
        for email, student in zip(emails, students):
            student.user.email = email
            students_updated.append(student.user)

        User.objects.bulk_update(students_updated, ['email'])

        students_with_filtered_email = Student.objects.filter(
            user__email__icontains=filter_params['email']
        ).count()

        response = self.client.get(f'{self.url}?email={filter_params["email"]}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], students_with_filtered_email)

        for student in response.data['results']:
            self.assertIn(filter_params['email'], student['email'])
