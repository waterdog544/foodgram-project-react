from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=16,
    )
    recipes = models.ManyToManyField(
        'Recipe',
        through='IngredientRecipe',
        verbose_name='Рецепты',
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        # related_name='recipes',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        # related_name='ingredients',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(1),)
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(1),),
    )
    tags = models.ManyToManyField(
        'Tag',
        through='TagRecipe',
        verbose_name='Тэги',
        blank=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        blank=True,
    )
    favorite_by_users = models.ManyToManyField(
        User,
        through='UserRecipe',
        verbose_name='Пользователи добавившие рецепт в избранное',
        blank=True,
    )

    def tag(self, obj):
        return obj.tags.all()

    def sum_favorite(self, obj):
        return obj.favorite_by_users.count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=16,
        help_text='Цвет в HEX'
    )
    slug = models.CharField(
        verbose_name='URl-aдрес',
        max_length=16,
        help_text='Уникальный слаг'
    )
    recipes = models.ManyToManyField(
        Recipe,
        through='TagRecipe',
        verbose_name='Рецепты',
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тэг'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_in_shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_by_users',
        verbose_name='Рецепт'
    )


class ShoppingCartIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Ингредиент'
    )
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(1),)
    )

    class Meta:
        verbose_name = 'Ингредиент в корзине'
        verbose_name_plural = 'Ингредиенты в корзинах'


class UserRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
