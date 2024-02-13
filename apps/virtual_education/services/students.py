from apps.virtual_education.models import Enrollment
from django.db.models import Q


class StudentService:
    @staticmethod
    def check_student_enrollment(student):
        # Verifica se o aluno já está matriculado em algum curso
        if Enrollment.objects.filter(
            ~Q(status='Desistiu'),
            student=student
        ).exists():
            raise Exception('O aluno está matriculado em um curso. Impossível apagar.')
