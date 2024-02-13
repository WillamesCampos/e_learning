from rest_framework import serializers
from apps.virtual_education.mixins.datetime_format import DateTimeFormatMixin
from apps.virtual_education.models import Course


class CourseSerializer(DateTimeFormatMixin, serializers.ModelSerializer):
    """
    Serializador para o modelo de Curso.
    """
    class Meta:
        model = Course
        fields = '__all__'
