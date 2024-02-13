from rest_framework import serializers
from apps.virtual_education.mixins.datetime_format import DateTimeFormatMixin
from apps.virtual_education.models import Enrollment


class EnrollmentSerializer(DateTimeFormatMixin, serializers.ModelSerializer):
    """
    Serializador para o modelo de Matrícula.
    """

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('status',)
