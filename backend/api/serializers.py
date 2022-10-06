import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe
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
        source='ingredient'
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
    is_subscribed = serializers.SerializerMethodField(read_only=True)

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
    is_favorited = serializers.SerializerMethodField(read_only=True,)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

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

    def get_is_favorited(self, obj):
        return obj.is_favorited(self.context['request'].user)

    def get_is_in_shopping_cart(self, obj):
        return obj.is_in_shopping_cart(self.context['request'].user)

    def create(self, validated_data):
        name = validated_data['name']
        author = self.context['request'].user
        if Recipe.objects.filter(
            name=name,
            author=author
        ).exists():
            raise serializers.ValidationError(
                f'У автора {author} уже есть рецепт {name}.'
            )
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
        recipe.tags_th.set(tags_obj)
        return recipe

    def ingredients_add(self, ingredients, recipe):
        for ingredient in ingredients:
            if IngredientRecipe.objects.filter(
                    recipe=recipe,
                    ingredient=ingredient['ingredient'],
            ).exists():
                recipe.delete()
                raise serializers.ValidationError(
                    f'Ингредиент {ingredient["ingredient"].name}'
                    f' уже добавлен в рецепт {recipe}'
                )
            IngredientRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
        return recipe

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
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

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


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'name',
            'measurement_unit',
            'amount'
        )
        read_only_fields = (
            'name',
            'measurement_unit',
            'amount')

    def get_name(self,):
        raise ValueError(self)
        pass

    def get_measurement_unit(self):
        pass

    def amount(self):
        raise ValueError(self)
        pass
