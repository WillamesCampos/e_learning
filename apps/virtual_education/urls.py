from django.urls import path, include
from rest_framework import routers

from .views.courses import CourseViewSet
from .views.enrollments import EnrollmentViewSet
from .views.students import StudentViewSet


router = routers.DefaultRouter()

router.register(
    prefix='students',
    viewset=StudentViewSet,
    basename='students'
)


router.register(
    prefix='courses',
    viewset=CourseViewSet,
    basename='courses'
)


router.register(
    prefix='enrollments',
    viewset=EnrollmentViewSet,
    basename='enrollments'
)


urlpatterns = [
    path('', include(router.urls))
]
