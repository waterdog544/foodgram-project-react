
import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.filters import RecipeFilter, SubsciptionsFilter
from api.permissions import (IsAdminOrReadOnly, IsAdminOrReadOnlyObj,
                             IsAuthorOrAdminOrReadOnly)
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeSerializer, ShoppingCartSerializer,
                             SubscriptionsSerializer, TagSerializer)
from recipes.models import (Ingredient, Recipe, ShoppingCartRecipe, Tag,
                            UserFavoriteRecipe)
from users.models import User


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def shopping_cart_get(request):
    user = request.user
    ingredients_val = Ingredient.objects.prefetch_related(
        'ingredient_recipes__recipe__shopping_cart_recipes__user'
    ).all().filter(
        ingredient_recipes__recipe__shopping_cart_recipes__user=user
    ).annotate(sum_amount=Sum('ingredient_recipes__amount')).values(
        'name', 'measurement_unit', 'sum_amount'
    )
    shopping_list = 'Список продуктов:\n\n'
    for i in ingredients_val:
        shopping_list = (
            shopping_list + chr(176) + ' ' + i['name']
            + ' (' + i['measurement_unit'] + ') - ' + str(i['sum_amount']) + '\n'
        )
    buffer = io.BytesIO()
    shopping_list_txt_name = ''.join(
        (''.join(user.email.split('@'))).split('.')
    ) + '.txt'
    buffer.write(shopping_list.encode('utf-8'))
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True,
        filename=shopping_list_txt_name
    )


class ShoppingCartViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'head', 'options')
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = []


    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        queryset = user.shopping_cart_recipes.select_related(
            'shopping_cart_recipes__recipe__ingreditnts',
            'shopping_cart_recipes__recipe__ingreditnts__ingredient',
        )
        return queryset


@api_view(('POST', 'DELETE'))
@permission_classes((IsAuthenticated,))
def shopping_cart_set(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
    except Exception as e:
        error = {'errors': f'{e} Рецепта c id = {recipe_id} нет в базе.'}
        raise ValidationError(error)
    user = request.user
    if request.method == 'POST':
        if ShoppingCartRecipe.objects.filter(
            user=user, recipe=recipe
        ).exists():
            error = {'errors': (
                f'Рецепт c id = {recipe_id} уже добавлен пользователем'
                f' {user} в корзину.'
            )}
            raise ValidationError(error)
        ShoppingCartRecipe.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    try:
        recipe_in_shoppiong_carte = get_object_or_404(
            ShoppingCartRecipe, user=user, recipe=recipe
        )
    except Exception:
        error = {'errors': (
            f'Рецепт c id = {recipe_id} не добавлен пользователем'
            f' {user} в корзину.'
        )}
        raise ValidationError(error)
    recipe_in_shoppiong_carte.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'head', 'options')
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = SubsciptionsFilter
    filterset_fileds = ('recipes',)

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
        return user.subscribers.prefetch_related(
            'recipes', 'recipes__tags_th'
        ).all()


@api_view(('POST', 'DELETE'))
@permission_classes((IsAuthenticated,))
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


@api_view(('POST', 'DELETE'))
@permission_classes((IsAuthenticated,))
def favorite_set(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
    except Exception as e:
        error = {'errors': f'{e} Рецепта c id = {recipe_id} нет в базе.'}
        raise ValidationError(error)
    user = request.user
    if request.method == 'POST':
        if UserFavoriteRecipe.objects.filter(
            user=user, recipe=recipe
        ).exists():
            error = {'errors': (
                f'Рецепт c id = {recipe_id} уже добавлен пользователем'
                f' {user} в избранные.'
            )}
            raise ValidationError(error)
        recipe.favorite_by_users.add(user)
        serializer = FavoriteSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    try:
        get_object_or_404(UserFavoriteRecipe, user=user, recipe=recipe)
    except Exception:
        error = {'errors': (
            f'Рецепт c id = {recipe_id} не добавлен пользователем'
            f' {user} в избранные.'
        )}
        raise ValidationError(error)
    recipe.favorite_by_users.remove(user)
    return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tags_th',).all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = RecipeFilter
    filterset_fileds = ('tags',)
    search_fields = ('^ingredients_th__name',)
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
