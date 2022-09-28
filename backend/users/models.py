from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
        help_text='Имя пользователя'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
        help_text='Фамилия пользователя'
    )
    email = models.EmailField(
        'email адрес',
        blank=False,
        help_text='Email адрес пользователя',
        unique=True
    )
    favorite_recipes = models.ManyToManyField(
        'recipes.Recipe',
        through='recipes.UserFavoriteRecipe',
        blank=True,
        verbose_name='Избранные рецепты'
    )
    subscriptions = models.ManyToManyField(
        'self',
        verbose_name='Подписки на авторов',
        blank=True,
        related_name='subcribers'
    )

    def __str__(self):
        return self.username

    def is_subscribed(self, anyuser):
        return self.subscriptions.filter(id=anyuser.id).exists()

    def is_favorited(self, anyrecipe):
        return self.favorite_recipes.filter(id=anyrecipe.id).exists()
    
    def is_in_shopping_cart(self, anyrecipe):
        return self.shopping_cart_recipes.filter(id=anyrecipe.id).exists()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
