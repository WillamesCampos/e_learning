from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.virtual_education.models import Enrollment
from apps.virtual_education.filters.enrollments import EnrollmentFilter
from apps.virtual_education.serializers.enrollments import EnrollmentSerializer
from apps.virtual_education.services.enrollments import EnrollmentService


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de matrículas.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EnrollmentFilter

    @swagger_auto_schema(
        operation_description="Cria uma nova matrícula de um aluno em um curso.",
        responses={
            status.HTTP_201_CREATED: "Matrícula criada com sucesso.",
            status.HTTP_400_BAD_REQUEST: "Erro ao criar a matrícula.",
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        headers = self.get_success_headers(serializer.validated_data)

        try:
            EnrollmentService.enroll_student(
                validated_data=serializer.validated_data
            )
        except Exception as exc:
            data = {'student': str(exc.args)}
            return Response(
                data=data, status=status.HTTP_400_BAD_REQUEST, headers=headers
            )
        self.perform_create(serializer)

        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @swagger_auto_schema(
        operation_description="Atualiza uma matrícula existente.",
    )
    def perform_update(self, serializer):
        instance = serializer.save()
        if 'score' in serializer.validated_data:
            EnrollmentService.complete_enrollment(
                instance.student, instance.course, instance.score
            )
        if 'student' in serializer.validated_data or 'course' in serializer.validated_data:
            EnrollmentService.enroll_student(serializer.validated_data)
        EnrollmentService.notify_course_owner(
            instance.course, new_enrollments=[instance.pk]
        )

        if 'justification' in serializer.validated_data:
            EnrollmentService.cancel_enrollment(
                instance.id, serializer.validated_data['justification']
            )

    @swagger_auto_schema(
        operation_description="Cancela uma matrícula existente.",
    )
    def cancel_enrollment(self, request, *args, **kwargs):
        instance = self.get_object()
        justification = request.data.get('justification')
        EnrollmentService.cancel_enrollment(instance.student, instance.course, justification)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Completa uma matrícula existente.",
    )
    def complete_enrollment(self, request, *args, **kwargs):
        instance = self.get_object()
        score = request.data.get('score')
        EnrollmentService.complete_enrollment(instance.student, instance.course, score)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Notifica os alunos sobre a quantidade de dias restantes para o término da matrícula.",
    )
    def notify_days_left(self, request):
        enrollment = self.get_object()
        EnrollmentService.notify_students_of_enrollment(enrollment)
