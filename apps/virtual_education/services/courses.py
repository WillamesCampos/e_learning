from apps.virtual_education.models import Enrollment


class CourseService:
    @staticmethod
    def notify_expiring_enrollments(course, days_remaining):
        # Notifica os alunos matriculados no curso sobre a expiração
        enrolled_students = Enrollment.objects.filter(course=course, date_close__isnull=True)
        for enrollment in enrolled_students:
            print(f'O curso {course.name} expirará em {days_remaining} dias. Matrícula: {enrollment.pk}')

    @staticmethod
    def notify_course_owner(course, started_enrolls=[], finished_enrolls=[]):
        pass

    @staticmethod
    def check_course_with_enrollments(course):
        if Enrollment.objects.filter(
            status='Andamento',
            course=course
        ).exists():
            raise Exception('O curso está com matrículas em andamento. As matrículas devem estar concluídas.')
