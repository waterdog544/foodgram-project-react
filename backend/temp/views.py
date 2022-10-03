from rest_framework.response import Response
from rest_framework import status
from functools import partial
from api.serializers import (
    IngredientSerializer,
    # RecipeReadSerializer,
    RecipeSerializer,
    RecipeNewSerializer,
    RecipeNew1Serializer,
    TagSerializer,
)

from recipes.models import (
    Ingredient,
    Recipe, Tag,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
)
from api.permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly


# class CustomUserViewSet(UserViewSet):
#     pagination_class = PageNumberPagination


# from backend.api.serializers import CustomUserSerializer, UserSerializer
# from backend.users import User


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return UserListSerializer
#         return UserSerializer

# class CustomUserViewSet(UserViewSet):
#     queryset = User.objects.all()
class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    serializer_class = RecipeNew1Serializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    # def get_serializer_class(self):
    #     # if self.action == 'create':
    #     # #     raise ValidationError(
    #     # #     f' {self.action} Необходимо добавить tag'
    #     # # )
    #     #     return RecipeNewSerializer
    #     # return RecipeSerializer
    #     return RecipeNew1Serializer

    # def perform_create(self, serializer):
    #     print(serializer.data)
    #     raise ValidationError(
    #         f' SELF {self} ACTION {self.action} INITIAL {serializer.initial_data["tags"]}'
    #         f' SERIALIZER{serializer}Необходимо добавить tag'
    #         f' DATA {serializer.data.get("tags")}'
    #     )
    #     return super().perform_create(serializer)
    
    def create(self, request, pk=None):
        try:
            tags = request.data.pop('tags')
        except Exception:
            raise ValidationError(
                'tags - обязательное поле. Необходимо добавить тэг.'
            )
        # tags = request.data.pop('tags')
        tags_dict = []
        for tag in tags:
            tags_dict.append({'tag': tag})
        request.data['tags'] = tags_dict
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    # def partial_update(self, request, pk=None):
    #     if tags in request.data:
    #         tags = request.data.pop('tags')
    #         tags_dict = []
    #         for tag in tags:
    #             tags_dict.append({'id': tag})
    #         request.data['tags'] = tags_dict
    #     recipe = self.get_object            
    #     serializer = RecipeSerializer(data=request.data,)
    #     if serializer.is_valid():

    #     raise ValidationError(
    #         f' SELF {request.data} '
    #         # f'ACTION {self.action} INITIAL {serializer.initial_data["tags"]}'
            # )
        # serialized = DemoSerializer(request.user, data=request.data, partial=True)
        # return Response(status=status.HTTP_202_ACCEPTED)
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = UserFavoriteRecipe.objects.select_related('recipe').all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['recipe'] = self.kwargs.get('recipe_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer
