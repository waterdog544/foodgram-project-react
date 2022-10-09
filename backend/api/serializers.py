import base64

from django.core.files.base import ContentFile
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from backend.settings import MIN_AMOUNT, MIN_TIME
from recipes.models import (Ingredient, IngredientRecipe, Recipe,
                            ShoppingCartRecipe, Tag, TagRecipe,
                            UserFavoriteRecipe)
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        validators = (
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=('name', 'measurement_unit')
            ),
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )
        validators = (
            UniqueTogetherValidator(
                queryset=Tag.objects.all(),
                fields=(
                    'name',
                    'color',
                    'slug'
                )
            ),
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(),
        slug_field='id',
        source='ingredient',
    )
    name = serializers.SlugRelatedField(
        slug_field='name', source='ingredient', read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        slug_field='measurement_unit', source='ingredient', read_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class TagRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='id',
        source='tag'
    )
    name = serializers.SlugRelatedField(
        slug_field='name', source='tag', read_only=True
    )
    color = serializers.SlugRelatedField(
        slug_field='color', source='tag', read_only=True
    )
    slug = serializers.SlugRelatedField(
        slug_field='slug', source='tag', read_only=True
    )

    class Meta:
        model = TagRecipe
        fields = ('id', 'name', 'color', 'slug')


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        read_only_fields = ('id',)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        read_only=True, method_name='get_is_subscribed')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return obj.is_subscribed(self.context['request'].user)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagRecipeSerializer(many=True)
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(
        read_only=True, method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True, method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_cooking_time(self, attrs):
        if attrs < MIN_TIME:
            raise ValidationError(
                f'Время приготовления не может быть меньше {MIN_TIME}'
            )
        return attrs

    def validate_ingredients(self, attrs):
        id_list = []
        for i in attrs:
            if i['ingredient'].id in id_list:
                raise ValidationError(
                    [{"id": [f'{i["ingredient"].name} повторяются.']}]
                )
            else:
                id_list.append(i['ingredient'].id)
            if i['amount'] < MIN_AMOUNT:
                raise ValidationError(
                    f'Количество {i["ingredient"].name} '
                    f'не может быть меньше {MIN_AMOUNT}'
                )
        return attrs

    def validate_name(self, name):
        author = self.context['request'].user
        if Recipe.objects.filter(
            name=name,
            author=author
        ).exists():
            raise serializers.ValidationError(
                f'У автора {author} уже есть рецепт {name}.'
            )
        return name

    def get_is_favorited(self, obj):
        return obj.is_favorited(self.context['request'].user)

    def get_is_in_shopping_cart(self, obj):
        return obj.is_in_shopping_cart(self.context['request'].user)

    @transaction.atomic
    def create(self, validated_data):
        author = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data,
            author=author
        )
        self.tags_add(tags=tags, recipe=recipe)
        self.ingredients_add(ingredients=ingredients, recipe=recipe)
        return recipe

    def tags_add(self, tags, recipe):
        tags_obj = []
        for tag in tags:
            tags_obj.append(tag['tag'])
        recipe.tag_through.set(tags_obj)
        return recipe

    def ingredients_add(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            self.tags_add(tags=tags, recipe=instance)

        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients_th.set([])
            self.ingredients_add(ingredients=ingredients, recipe=instance)
        return instance


class FavoriteSerializerNew(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(method_name='id')
    name = serializers.SerializerMethodField(method_name='name')
    image = serializers.SerializerMethodField(method_name='image')
    cooking_time = serializers.SerializerMethodField(
        method_name='cooking_time'
    )
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='id',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserFavoriteRecipe
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
        write_only_fields = ('user', 'recipes')

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            user = request.user
            recipe = self.context.get('view').kwargs.get('recipe_id')
            if not user.is_authenicated:
                raise ValidationError(
                    'Пользователь не авторизован'
                )
            if UserFavoriteRecipe.objects.filter(
                user=user, recipe=recipe
            ).exists():
                raise ValidationError(
                    f'Рецепт c id = {recipe.id} уже добавлен пользователем'
                    f' {user} в корзину.'
                )
        return data

    def get_id(self, recipe):
        return recipe.id

    def get_name(self, recipe):
        return recipe.name

    def get_image(self, recipe):
        return Base64ImageField(
            recipe.image, context=self.context.get('request')
        )


class ShoppingCartSerializer(FavoriteSerializerNew):

    class Meta:
        model = UserFavoriteRecipe
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
        write_only_fields = ('user', 'recipes')


class FavoriteSerializer(RecipeSerializer):
    image = Base64ImageField(read_only=True)
    favorite_by_users = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', 'favorite_by_users')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionsSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, author):
        return author.recipes_count

    def get_recipes(self, author):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        if recipes_limit:
            queryset = author.recipes.all()[:int(recipes_limit)]
            return FavoriteSerializer(queryset, many=True).data
        queryset = author.recipes.all()
        return FavoriteSerializer(queryset, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return obj.is_subscribed(request.user)


def get_user(pk):
    users = User.objects.filter(pk=pk)
    if not users.exists():
        error = {'errors': f'Пользователя c id = {pk} нет в базе.'}
        raise ValidationError(error)
    return users[0]


def get_recipe(pk):
    recipe = Recipe.objects.filter(pk=pk)
    if not recipe.exists():
        error = {'errors': f'Рецепта c id = {pk} нет в базе.'}
        raise ValidationError(error)
    return recipe[0]


def check_is_favorited(user, recipe):
    if UserFavoriteRecipe.objects.filter(
        user=user, recipe=recipe
    ).exists():
        error = {'errors': (
            f'Рецепт c id = {recipe.id} уже добавлен пользователем'
            f' {user} в избранные.'
        )}
        raise ValidationError(error)


def get_recipe_in_favorite(user, recipe):
    recipe_in_favorite = UserFavoriteRecipe.objects.filter(
        user=user, recipe=recipe
    )
    if not recipe_in_favorite.exists():
        error = {'errors': (
            f'Рецепт c id = {recipe.id} не добавлен пользователем'
            f' {user} в избранные.'
        )}
        raise ValidationError(error)
    return recipe_in_favorite[0]


def check_is_in_shopping_cart(user, recipe):
    if ShoppingCartRecipe.objects.filter(
        user=user, recipe=recipe
    ).exists():
        error = {'errors': (
            f'Рецепт c id = {recipe.id} уже добавлен пользователем'
            f' {user} в корзину.'
        )}
        raise ValidationError(error)


def get_recipe_in_shopping_cart(user, recipe):
    recipe_in_shopping_cart = ShoppingCartRecipe.objects.filter(
        user=user, recipe=recipe
    )
    if not recipe_in_shopping_cart.exists():
        error = {'errors': (
            f'Рецепт c id = {recipe.id} не добавлен пользователем'
            f' {user} в корзину.'
        )}
        raise ValidationError(error)
    return recipe_in_shopping_cart[0]


def check_is_subscribed(user, author):
    if user.is_subscribed(author):
        error = {'errors': (
            f'Пользователь "{user}" уже подписан на'
            f' автора {author.username}.'
        )}
        raise ValidationError(error)


def check_is_not_subscribed(user, author):
    if not user.is_subscribed(author):
        error = {'errors': (
            f'Пользователь {user} не подписан на автора c id = {user.id}.'
        )}
        raise ValidationError(error)
