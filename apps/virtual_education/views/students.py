from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from apps.virtual_education.models import Student
from apps.virtual_education.serializers.students import StudentSerializer
from apps.virtual_education.filters.students import StudentFilter
from apps.virtual_education.services.students import StudentService


class StudentViewSet(ModelViewSet):
    """
    API para gerenciamento de alunos.
    """
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

    @swagger_auto_schema(
        operation_description="Exclui um aluno.",
    )
    def perform_destroy(self, instance):
        StudentService.check_student_enrollment(student=instance)
        return super().perform_destroy(instance)

    @swagger_auto_schema(
        operation_description="Exclui um aluno existente.",
        responses={
            status.HTTP_204_NO_CONTENT: "Aluno excluído com sucesso.",
            status.HTTP_400_BAD_REQUEST: "Erro ao excluir o aluno.",
        },
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Exception as exc:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=str(exc)
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
