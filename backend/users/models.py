from django.contrib.auth.models import AbstractUser
from django.db import models
from recipes.models import Recipe


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
    favorit_recipes = models.ManyToManyField(
        Recipe,
        through='UserRecipe',
        blank=True,
        null=True,
        verbose_name='Избранные рецепты'
    )
    subscriptions = models.ManyToManyField(
        User,
        through='Subscribe',
        verbose_name='Подписки на авторов',
    )
    subcribers = models.ManyToManyField(
        User,
        through='Subscribe',
        verbose_name='Подписчики',
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
