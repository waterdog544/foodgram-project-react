from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response

class RecipesLimitPagination(LimitOffsetPagination):
    limit_query_param = 'recipes_limit'

    # def get_paginated_response_schema(self, schema):
    #     return {
    #         'type': 'object',
    #         'properties': {
    #             'recipes': schema,
    #         },
    #     }

    # def get_paginated_response(self, data):
    #     return Response(OrderedDict([
    #         ('recipes', data)
    #     ]))    
