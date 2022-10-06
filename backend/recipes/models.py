from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import format_html

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
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            ),
        )


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(0.1),)
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe'
            ),
        )


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
        verbose_name='Время приготовления, мин.',
        validators=(MinValueValidator(1),),
    )
    tags_th = models.ManyToManyField(
        'Tag',
        through='TagRecipe',
        verbose_name='Тэги',
    )
    ingredients_th = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
    )
    favorite_by_users = models.ManyToManyField(
        User,
        through='UserFavoriteRecipe',
        verbose_name='Пользователи, добавившие рецепт в избранное',
        blank=True,
    )

    def image_tag(self):
        return format_html('<img src="%s">' % self.image.url)
    image_tag.short_description = 'Картинка'

    @property
    def added_to_favorite(self):
        return self.favorite_by_users.count()

    def is_favorited(self, anyuser):
        return self.favorite_by_users.filter(id=anyuser.id).exists()

    def is_in_shopping_cart(self, anyuser):
        return self.shopping_cart_recipes.filter(user=anyuser.id).exists()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name', ),
                name='unique_author_name'
            ),
        )


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
        verbose_name_plural = 'Список тэгов'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'slug'),
                name='unique_name_slug'
            ),
        )


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тэг'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Тэги рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=('tag', 'recipe'),
                name='unique_tag_recipe'
            ),
        )


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes',
        verbose_name='Корзина пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes',
        verbose_name='Рецепт в корзине'
    )

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class UserFavoriteRecipe(models.Model):
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

    def __str__(self):
        return f'{self.user.username} {self.recipe.name}'

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избраннные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe'
            ),
        )
