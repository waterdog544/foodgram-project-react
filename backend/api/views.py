from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.paginations import PageLimitPagination
from api.permissions import (IsAdminOrReadOnly, IsAdminOrReadOnlyObj,
                             IsAuthorOrAdminOrReadOnly)
from api.serializers import (FavoriteSerializer, FavoriteSerializerNew,
                             IngredientSerializer, RecipeSerializer,
                             ShoppingCartSerializer, SubscriptionsSerializer,
                             TagSerializer, check_is_favorited,
                             check_is_in_shopping_cart,
                             check_is_not_subscribed, check_is_subscribed,
                             get_recipe, get_recipe_in_favorite,
                             get_recipe_in_shopping_cart, get_user)
from recipes.models import Ingredient, Recipe, ShoppingCartRecipe, Tag
from users.models import Subscriptions, User


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
            f'{shopping_list} {chr(176)} {i["name"]} '
            f'({i["measurement_unit"]}) - {str(i["sum_amount"])}\n'
        )
    response = HttpResponse()
    response.write(content=shopping_list)
    return HttpResponse(response, content_type='text/plain')


@api_view(('POST', 'DELETE'))
@permission_classes((IsAuthenticated,))
def shopping_cart_set(request, recipe_id):
    recipe = get_recipe(pk=recipe_id)
    user = request.user
    if request.method == 'POST':
        check_is_in_shopping_cart(user=user, recipe=recipe)
        ShoppingCartRecipe.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    recipe_in_shopping_cart = get_recipe_in_shopping_cart(
        user=user, recipe=recipe
    )
    recipe_in_shopping_cart.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'head', 'options')
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    pagination_class = PageLimitPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            subscribers__follower=user
        ).prefetch_related(
            'recipes', 'recipes__tags__tag'
        ).all()


@api_view(('POST', 'DELETE'))
@permission_classes((IsAuthenticated,))
def subscribe_set(request, user_id):
    author = get_user(pk=user_id)
    user = request.user
    if request.method == 'POST':
        check_is_subscribed(user=user, author=author)
        Subscriptions.objects.create(author=author, follower=user)
        author.save()
        serializer = SubscriptionsSerializer(
            author,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    check_is_not_subscribed(author=author, user=user)
    Subscriptions.objects.filter(author=author, follower=user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'delete', 'head', 'options')
    pagination_class = None
    serializer_class = FavoriteSerializerNew
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        return recipe.favorite.all()


class ShoppingCartViewSet(FavoriteViewSet):
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        return recipe.favorite.all()


@api_view(('POST', 'DELETE'))
@permission_classes((IsAuthenticated,))
def favorite_set(request, recipe_id):
    recipe = get_recipe(pk=recipe_id)
    user = request.user
    if request.method == 'POST':
        check_is_favorited(user=user, recipe=recipe)
        recipe.favorite_by_users.add(user)
        serializer = FavoriteSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    recipe_in_favorite = get_recipe_in_favorite(user=user, recipe=recipe)
    recipe_in_favorite.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('tag_through',).all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = RecipeFilter
    filterset_fileds = ('tags',)
    search_fields = ('^ingredients_th__name',)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    @transaction.atomic
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

    @transaction.atomic
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
