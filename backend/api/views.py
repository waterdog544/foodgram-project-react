
from urllib import request
from rest_framework import authentication, permissions
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status

from api.serializers import (

    IngredientSerializer,

    RecipeSerializer,
    TagSerializer,
    FavoriteSerializer,
    SubscriptionsSerializer
    
)
from api.filters import (
    RecipeFilter,
    # RecipeSearch
    )

from rest_framework import mixins


from users.models import User
from recipes.models import (
    Ingredient,
    Recipe, Tag,
    UserFavoriteRecipe,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated
)
from api.permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly, IsAdminOrReadOnlyObj
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
   
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={'request': self.request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={'request': self.request}
        )
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return user.subscribers.all()


@api_view(['POST', 'DELETE'])
def subscribe_set(request, user_id):
    try:
        author = get_object_or_404(User, pk=user_id)
    except Exception as e:
        error = {'errors': f'{e} Автора c id = {user_id} нет в базе.'}
        raise ValidationError(error)
    user = request.user
    if request.method == 'POST':
        if author.subscribers.filter(id=user.id).exists():
            error = {'errors': (
                f'Пользователь "{user}" уже подписан на'
                f' автора {author.username}.'
            )}            
            raise ValidationError(error)
        author.subscribers.add(user)
        author.save()
        serializer = SubscriptionsSerializer(
            author,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if not user.is_subscribed(author):
        error = {'errors': (
            f'Пользователь {user} не подписан на автора c id = {user_id}.'
            f' {user} в избранные'
        )}
        raise ValidationError(error)
    author.subscribers.remove(user)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
def favorite_set(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
    except Exception as e:
        error = {'errors': f'{e} Рецепта c id = {recipe_id} нет в базе.'}
        raise ValidationError(error)
    user = request.user
    if request.method == 'POST':
        recipe.favorite_by_users.add(user)
        serializer = FavoriteSerializer(recipe, )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    try:
        get_object_or_404(UserFavoriteRecipe, user=user, recipe=recipe)
    except Exception:
        error = {'errors': (
            f'Рецепт c id = {recipe_id} не добавлен пользователем'
            f' {user} в избранные'
        )}
        raise ValidationError(error)
    recipe.favorite_by_users.remove(user)
    return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = RecipeFilter
    search_fields = ('^ingredients_th__name',)
    filterset_fileds = ('tags',)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def create(self, request, pk=None):
        self.tags_add_dict(request=request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        self.tags_add_dict(request=request)
        return self.update(request, *args, **kwargs)

    def tags_add_dict(self, request):
        if 'tags' in request.data:
            tags = request.data.pop('tags', False)
            tags_dict = []
            for tag in tags:
                tags_dict.append({'id': tag})
            request.data['tags'] = tags_dict
        return request





