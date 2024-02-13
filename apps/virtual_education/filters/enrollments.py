from django_filters import rest_framework as filters
from apps.virtual_education.models import Enrollment


class EnrollmentFilter(filters.FilterSet):

    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    student = filters.UUIDFilter(field_name='student')
    course = filters.UUIDFilter(field_name='course', lookup_expr='exact')
    date_enroll = filters.DateFilter(field_name='date_enroll', lookup_expr='gte')
    date_close = filters.DateFilter(field_name='date_close', lookup_expr='gte')

    class Meta:
        model = Enrollment
        fields = ['status', 'student', 'course', 'date_enroll', 'date_close']
