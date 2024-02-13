from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.virtual_education.filters.courses import CourseFilter
from apps.virtual_education.models import Course
from apps.virtual_education.serializers.courses import CourseSerializer
from apps.virtual_education.services.courses import CourseService


class CourseViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de cursos.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

    @swagger_auto_schema(
        operation_description="Exclui um curso, verificando se possui matrículas associadas.",
        responses={status.HTTP_204_NO_CONTENT: "Curso excluído com sucesso."},
    )
    def perform_destroy(self, instance):
        CourseService.check_course_with_enrollments(course=instance)
        return super().perform_destroy(instance)

    @swagger_auto_schema(
        operation_description="Exclui um curso.",
        responses={
            status.HTTP_204_NO_CONTENT: "Curso excluído com sucesso.",
            status.HTTP_400_BAD_REQUEST: "Erro ao excluir o curso.",
        },
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except Exception as exc:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=str(exc.args)
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Notifica as matrículas que estão próximas do vencimento.",
        responses={status.HTTP_204_NO_CONTENT: "Notificação enviada com sucesso."},
    )
    def notify_expiring_enrollments(self, request, *args, **kwargs):
        instance = self.get_object()
        days_remaining = request.data.get('days_remaining')
        CourseService.notify_expiring_enrollments(instance, days_remaining)
        return Response(status=status.HTTP_204_NO_CONTENT)
