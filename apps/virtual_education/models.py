import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from drf_yasg.utils import swagger_auto_schema


class User(AbstractUser):
    """
    Usuário do sistema.
    """
    nickname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @swagger_auto_schema(auto_schema=None)
    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email

        if self.nickname:
            self.first_name = self.nickname
        return super().save(*args, **kwargs)


class Profile(models.Model):
    """
    Perfil de usuário.
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Student(Profile):
    """
    Aluno.
    """
    avatar = models.ImageField(upload_to='media/student_avatars/', null=True)

    def __str__(self):
        return self.user.email


class Owner(Profile):
    """
    Proprietário do curso.
    """
    avatar = models.ImageField(upload_to='media/owner_avatars/', null=True)
    courses = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='owners'
    )

    def __str__(self):
        return self.user.email


class Course(models.Model):
    """
    Curso.
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    holder_image = models.ImageField(upload_to='course_images/', null=True)
    duration = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """
    Matrícula de um aluno em um curso.
    """
    STATUS_CHOICES = (
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
        ('Andamento', 'Andamento'),
        ('Desistiu', 'Desistiu'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    date_enroll = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField()
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Andamento')
    justification = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}"
