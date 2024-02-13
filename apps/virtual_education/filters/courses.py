from django_filters import rest_framework as filters
from apps.virtual_education.models import Course


class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'name': ['icontains'],
            'duration': ['exact', 'gte', 'lte'],
            'date_created': ['exact', 'gte', 'lte'],
            'date_updated': ['exact', 'gte', 'lte'],
        }
