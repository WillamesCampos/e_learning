from django_filters import rest_framework as filters
from apps.virtual_education.models import Student


class StudentFilter(filters.FilterSet):

    date_created = filters.DateFilter(
        field_name='user__date_created', lookup_expr='date__gte'
    )
    nickname = filters.CharFilter(
        field_name='user__nickname', lookup_expr='icontains'
    )
    email = filters.CharFilter(
        field_name='user__email', lookup_expr='icontains'
    )

    class Meta:
        model = Student
        fields = ['date_created', 'nickname', 'email']
