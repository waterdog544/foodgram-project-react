from asyncore import write
from wsgiref.validate import validator
from rest_framework.serializers import ValidationError
# import webcolors
import base64
from django.core.files.base import ContentFile
# import re
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
# from importlib.metadata import files

from recipes.models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    TagRecipe
)
from rest_framework import serializers
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        queryset =Ingredient.objects.all(),
        slug_field='id',
        source='ingredient'
    )
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class TagNewSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TagRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit
# class IngredientRecipeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = IngredientRecipe
#         fields = ('id', 'amount')


# class IngredientSerializer(serializers.ModelSerializer):
#     ingredient_recipes = IngredientRecipeSerializer
#     # amount = serializers.SerializerMethodField()

#     class Meta:
#         model = Ingredient
#         fields = (
#             'id', 'name', 'measurement_unit',
#             'ingredient_recipes',
#         )

#     # def get_amount(self, obj):
#     #     # recipe_id = self.kwargs.get('recipe_id')
#     #     recipe_id = self.context['request']
#     #     return f'{obj.id} {recipe_id}'
#     #     # return obj.ingredient_recipes.get(recipe=recipe_id).amount

#     # def get_amount(self, obj):
#     #     # recipe_id = self.kwargs.get('recipe_id')
#     #     recipe_id = self.context['request']
#     #     return f'{obj.id} {recipe_id}'
#     #     # return obj.ingredient_recipes.get(recipe=recipe_id).amount

class TagObjSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields ='__all__'



class TagSerializer(serializers.ModelSerializer):
    # id = serializers.SlugRelatedField(
    #     queryset=Tag.objects.all(),
    #     slug_field='id',
    #     source='tag'
    # )
    # id = serializers.PrimaryKeyRelatedField( read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    color = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SerializerMethodField(read_only=True)
    tag = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Tag.objects.all())
    
    
    class Meta:
        model = TagRecipe
        fields = ('id', 'name', 'color', 'slug',
            'tag'
        )
            
    def get_id(self, obj):
        return obj.tag.id

    def get_name(self, obj):
        return obj.tag.name

    def get_color(self, obj):
        return obj.tag.color
    
    def get_slug(self, obj):
        return obj.tag.slug


    # def validate_color(self, value):
    #     match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
    #     if not match:
    #         raise serializers.ValidationError(
    #             'Строка не соответсвует HEX-формату'
    #         )
    #     return value


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


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
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientSerializer(many=True)
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


# class TagRecipeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = TagRecipe
#         fields = ('id',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',

        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeNewSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    # tags = TagRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        # a=self.context['request']
        # # if validated_data['tags']:
        # raise serializers.ValidationError(
        #     f' {a} {validated_data} Необходимо добавить ингредиенты'
        # )
        # c = self.context['request'].user
        # b = self.initial_data
        # a = validated_data

        # raise serializers.ValidationError(
        #     f' init{b} valid{a} valid without{validated_data} Необходимо добавить ингредиенты'
        # )
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data, author=self.context['request'].user)
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо добавить ингредиенты'
            )
        for ingredient in ingredients:
        #     raise serializers.ValidationError(
        #     f' init{ingredient["ingredient"].id}  Необходимо добавить ингредиенты'
        # )
        #     if not Ingredient.objects.filter(id=ingredient['ingredient']).exists():
        #         raise serializers.ValidationError(
        #             'Ингредиента нет в базе'
        #         )
            IngredientRecipe.objects.create(
                ingredient=ingredient['ingredient'],
                recipe=recipe,
                amount=ingredient['amount'])
        # if not tags:
        #     raise serializers.ValidationError(
        #         'Необходимо добавить тэг'
        #     )
        for tag in tags:
        #     if not Tag.objects.filter(id=tag).exists():
        #         raise serializers.ValidationError(
        #             'Тэга нет в базе'
        #         )
            TagRecipe.objects.create(tag=tag, recipe=recipe)
        return recipe


class RecipeNew1Serializer(serializers.ModelSerializer):

    image = Base64ImageField()
    tags = TagSerializer(many=True)
    # tags = serializers.HiddenField(
    #         default = serializers.PrimaryKeyRelatedField(
    #             many=True,
    #             queryset=Tag.objects.all()
    #             )
    #     )

    # tags = serializers.SlugRelatedField(
    #     many=True,
    #     queryset=Tag.objects.all(),
    #     slug_field='id'
        
    # )
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientSerializer(many=True)
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
        # try:
        #     tags = self.initial_data.pop('tags')
        # except Exception:
        #     raise serializers.ValidationError(
        #         'tags - обязательное поле. Необходимо добавить тэг.'
        #     )
        # if not tags:
        #     raise serializers.ValidationError(
        #         'tags - не может быть пустым. Необходимо добавить тэг.'
        #     )
        tags = validated_data.pop('tags')
        # raise serializers.ValidationError(
        #         f'{tags} .'
        #     )
        ingredients = validated_data.pop('ingredients')
        name = validated_data['name']
        author = self.context['request'].user
        if Recipe.objects.filter(
            name=name,
            author=author
        ).exists():
            raise serializers.ValidationError(
                f'У автора {author} уже есть рецепт {name}.'
            )
        recipe = Recipe.objects.create(
            **validated_data,
            author=author
        )
        # raise serializers.ValidationError(
        #             f'{tags} - должно быть целое число.'
        #         )
        # recipe.tags_th.set(tags)
        for tag in tags:
            TagRecipe.objects.create(recipe=recipe, tag=tag['tag'])
        # tags_obj = []
        # for tag in tags:
        #     if not isinstance(tag, int):
        #         recipe.delete()
        #         raise serializers.ValidationError(
        #             '{tag} - должно быть целое число.'
        #         )
        #     try:
        #         tag_obj = get_object_or_404(Tag, pk=tag)
        #     except Exception as e:
        #         recipe.delete()
        #         raise serializers.ValidationError(
        #             f'{e} "id": {tag} - тега нет в базе'
        #         )
        #     tags_obj.append(tag_obj)
        #     recipe.tags_th.set(tags_obj)

            # if TagRecipe.objects.filter(
            #     recipe=recipe,
            #     tag=tag_obj
            # ).exists():
            #     recipe.delete()
            #     raise serializers.ValidationError(
            #         f'Тэг {tag} уже добавлен к рецепту {recipe}'
            #     )
            # TagRecipe.objects.create(tag=tag_obj, recipe=recipe)        
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
        # if 'tags' in self.initial_data:
        #     tags = self.initial_data.pop('tags')
        #     tags_obj = []
        #     for tag in tags:
        #         if not isinstance(tag, int):
        #             raise serializers.ValidationError(
        #                 '{tag} - должно быть целое число.'
        #             )
        #         try:
        #             tag_obj = get_object_or_404(Tag, pk=tag)
        #         except Exception as e:                
        #             raise serializers.ValidationError(
        #                 f'{e} "id": {tag} - тега нет в базе'
        #             )
        #         tags_obj.append(tag_obj)
        #     instance.tags_th.set(tags_obj)


        # if 'tags' in self.initial_data:
        #     tags = self.initial_data.pop('tags')            
        #     for tag in tags:
        #         if not isinstance(tag, int):
        #             raise serializers.ValidationError(
        #                 '{tag} - должно быть целое число.'
        #             )
        #         try:
        #             tag_obj = get_object_or_404(Tag, pk=tag)
        #         except Exception as e:
        #             raise serializers.ValidationError(
        #                 f'{e} "id": {tag} - тега нет в базе'
        #             )
        #         TagRecipe.objects.get_or_create(recipe=instance, tag=tag_obj)
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            for ingredient in ingredients:
                if IngredientRecipe.objects.filter(
                        recipe=instance,
                        ingredient=ingredient['ingredient'],
                ).exists():
                    IngredientRecipe.objects.filter(
                        recipe=instance,
                        ingredient=ingredient['ingredient'],
                    ).update(amount=ingredient['amount'])
                else:
                    IngredientRecipe.objects.create(
                        recipe=instance,
                        ingredient=ingredient['ingredient'],
                        amount=ingredient['amount']
                    )
        return instance




    #     # raise serializers.ValidationError(f'{self.initial_data}')
    #     # a=self.context['request']
    #     # # if validated_data['tags']:
    #     # raise serializers.ValidationError(
    #     #     f' {a} {validated_data} Необходимо добавить ингредиенты'
    #     # )
    #     # c = self.context['request'].user
    #     # b = self.initial_data
    #     # # a = validated_data

    #     # raise serializers.ValidationError(
    #     #     f' {c} {b} init {self.data} valid{validated_data}'
    #     #     # f' valid without{validated_data} Необходимо добавить ингредиенты'
    #     # )
    #     data = self.initial_data
    #     # try:
    #     #     ingredients = validated_data.pop('ingredients')
    #     # except Exception:
    #     #     raise serializers.ValidationError(
    #     #         'ingredients - обязятельное поле. Необходимо добавить ингредиенты.'
    #     #     )

    #     try:
    #         tags = data.pop('tags')
    #     except Exception:
    #         raise serializers.ValidationError(
    #             'tags - обязательное поле. Необходимо добавить тэг.'
    #         )
    #     if not tags:
    #         raise serializers.ValidationError(
    #             'Необходимо добавить тэг'
    #         )
    #     # if not ingredients:
    #     #     raise serializers.ValidationError(
    #     #         'Необходимо добавить ингредиенты'
    #     #     )
    #     name = validated_data['name']
    #     author = self.context['request'].user
    #     if Recipe.objects.filter(
    #         name=name,
    #         author=author
    #     ).exists():
    #         raise serializers.ValidationError(
    #             f'У автора {author} уже есть рецепт {name}.'
    #         )
    #     recipe = Recipe.objects.create(
    #         **validated_data,
    #         author=author
    #     )
    #     # for ingredient in ingredients:
    #     #     try:
    #     #         ingredient_obj = get_object_or_404(
    #     #             Ingredient,
    #     #             pk=ingredient['id']
    #     #         )
    #     #     except Exception as e:
    #     #         recipe.delete()
    #     #         raise serializers.ValidationError(
    #     #             f'{e} "id": {ingredient["id"]} - ингредиента нет в базе'
    #     #         )
    #     #     IngredientRecipe.objects.create(
    #     #         ingredient=ingredient_obj,
    #     #         recipe=recipe,
    #     #         amount=ingredient['amount']
    #     #     )
    #     for tag in tags:
    #         try:
    #             tag_obj = get_object_or_404(Tag, pk=tag)
    #         except Exception as e:
    #             recipe.delete()
    #             raise serializers.ValidationError(
    #                 f'{e} "id": {tag} - тега нет в базе'
    #             )
    #         TagRecipe.objects.create(tag=tag_obj, recipe=recipe)
    #     return recipe
        

     



    # 




# class Hex2NameColor(serializers.Field):
#     def to_representation(self, value):
#         return value

#     def to_internal_value(self, data):
#         try:
#             webcolors.hex_to_name(data)
#         except ValueError:
#             raise serializers.ValidationError('Цвета нет в библиотеке')
#         return data

class FavoriteSerializer(serializers.ModelSerializer, Base64ImageField):
    id = serializers.SlugRelatedField(
        source='recipe',
        slug_field='id',
        # queryset=UserFavoriteRecipe.objects.all(),
        read_only=True
    )
    name = serializers.SlugRelatedField(
        source='recipe',
        slug_field='name',
        # queryset=UserFavoriteRecipe.objects.all(),
        read_only=True
    )
    image_obj = serializers.SerializerMethodField(source='recipe', read_only=True)
    # image_obj = serializers.HiddenField(
    #     default=serializers.SlugRelatedField(
    #         source='recipe',
    #         slug_field='image',
    #         read_only=True
    #     ),
    # )
    # image_obj = serializers.SlugRelatedField(
    #         source='recipe',
    #         slug_field='image',
    #         read_only=True
    #     )
    # image = Base64ImageField(source='image_obj', read_only=True)
    # image = Base64ImageField(
    #     serializers.SlugRelatedField(
    #         source='recipe',
    #         slug_field='image',
    #         # queryset=UserFavoriteRecipe.objects.all(),
    #         read_only=True
    #     ).slug_field
    # )
    
    cooking_time = serializers.SlugRelatedField(
        source='recipe',
        slug_field='cooking_time',
        # queryset=UserFavoriteRecipe.objects.all(),
        read_only=True
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    


    class Meta:
        model = UserFavoriteRecipe
        fields = ('id',
        'name',
        # 'image',
        'image_obj',
        'cooking_time',
        'recipe',
        'user',        
        )
        write_only_fields = ('recipe', 'user')
    
    def get_image_obj(self, obj):
        data = obj.recipe.image
        # return data
        # use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
        
        # raise ValueError (data, 'obj.recipe.image', data.url)
        return data.to_representation(data.url)

        return self.to_internal_value(data={'recipe':obj.recipe.pk})