from rest_framework import serializers
from apps.virtual_education.models import Student, User
from apps.virtual_education.mixins.datetime_format import DateTimeFormatMixin


class StudentSerializer(DateTimeFormatMixin, serializers.ModelSerializer):
    """
    Serializador para o modelo de Estudante.
    """

    nickname = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)

    class Meta:
        model = Student
        exclude = ('user',)

    def get_user_data(self, validated_data):
        """
        Obtém os dados do usuário a partir dos dados validados.
        """
        user_data = {}

        user_fields = ['nickname', 'phone', 'email']

        for field in user_fields:
            if validated_data.get(field):
                user_data.update({field: validated_data[field]})

        return user_data

    def clean_validated_data(self, validated_data):
        """
        Remove os campos de usuário dos dados validados.
        """
        for field in ['nickname', 'email', 'phone']:
            try:
                validated_data.pop(field)
            except KeyError:
                continue

        return validated_data

    def to_representation(self, instance):
        """
        Converte a instância em uma representação serializável.
        """
        return {
            'id': instance.id,
            'nickname': instance.user.nickname,
            'phone': instance.user.phone,
            'email': instance.user.email
        }

    def create(self, validated_data):
        """
        Cria uma nova instância de Estudante e seu respectivo Usuário.
        """
        user_data = self.get_user_data(validated_data)
        user = User.objects.create(**user_data)

        self.clean_validated_data(validated_data)

        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        """
        Atualiza a instância de Estudante e seu respectivo Usuário.
        """
        user_data = self.get_user_data(validated_data)

        user = instance.user
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()

        self.clean_validated_data(validated_data)

        student = super().update(instance, validated_data)
        return student
