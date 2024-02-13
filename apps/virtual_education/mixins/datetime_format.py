from rest_framework import serializers


class DateTimeFormatMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, serializers.DateTimeField):
                field.format = '%d/%m/%Y %H:%M:%S'
