from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi


class CustomPagination(PageNumberPagination):
    """
    Paginação personalizada para a API.
    """

    page_query_param = 'pagina'
    page_size_query_param = 'tamanho'
    page_size = 10

    page_size_parameter = openapi.Parameter(
        name='tamanho',
        in_=openapi.IN_QUERY,
        description='Número de resultados retornados por página.',
        type=openapi.TYPE_INTEGER,
        format=openapi.FORMAT_INT32
    )

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'description': 'Número total de objetos encontrados.'
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'description': 'URL para a próxima página de resultados.'
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'description': 'URL para a página anterior de resultados.'
                },
                'results': schema,
            }
        }
