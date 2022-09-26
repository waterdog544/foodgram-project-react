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
        through='recipes.UserRecipe',
        blank=True,
        verbose_name='Избранные рецепты'
    )
    subscriptions = models.ManyToManyField(
        'self',
        verbose_name='Подписки на авторов',
        related_name='subcribers'
    )


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
