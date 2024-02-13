from datetime import datetime
from apps.virtual_education.models import Enrollment


class EnrollmentService:
    @staticmethod
    def enroll_student(validated_data):
        # Verifica se o aluno já está matriculado em algum curso
        student = validated_data['student']

        if Enrollment.objects.filter(
            status='Andamento',
            student=student,
        ).exists():
            raise Exception('O aluno já está matriculado em um curso.')

    @staticmethod
    def cancel_enrollment(id, justification):
        # Verifica se o aluno está matriculado no curso
        enrollment = Enrollment.objects.get(id=str(id))
        enrollment.justification = justification
        enrollment.date_close = datetime.now()
        enrollment.status = 'Desistiu'
        enrollment.save()

    @staticmethod
    def complete_enrollment(student, course, score):
        # Verifica se o aluno está matriculado no curso
        enrollment = Enrollment.objects.get(
            student=student, course=course, status='Andamento'
        )
        enrollment.score = score
        if score is not None and score < 6:
            enrollment.status = 'Reprovado'
        else:
            enrollment.status = 'Aprovado'
        enrollment.date_close = datetime.now()
        enrollment.save()

    @staticmethod
    def expire_course(course, days_remaining):
        # Notifica os alunos matriculados no curso sobre a expiração
        enrolled_students = Enrollment.objects.filter(
            course=course, date_close__isnull=True
        )
        for enrollment in enrolled_students:
            print(f'O curso {course.name} expirará em {days_remaining} dias. Matrícula: {enrollment.pk}')

    @staticmethod
    def notify_course_owner(course, new_enrollments):
        # Notifica o proprietário do curso sobre novas matrículas
        print(f'O curso {course.name} possui novas matrículas: {new_enrollments}')

    @staticmethod
    def notify_students_of_enrollment(enrollment):
        days_left = (enrollment.date_close - datetime.datetime.now().date()).days

        message = f"Faltam {days_left} dias para o término do curso {enrollment.course.name}"

        return message
