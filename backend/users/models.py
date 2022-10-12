from django.contrib.auth.models import AbstractUser
from django.db import models


class Subscriptions(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )
    follower = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )

    def __str__(self):
        return f'{self.follower} на {self.author} '

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'follower'),
                name='unique_author_follower'
            ),
        )


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

    def __str__(self):
        return self.username

    def is_subscribed(self, anyuser):
        return self.subscribers.filter(follower=anyuser.id).exists()

    @property
    def recipes_count(self):
        return self.recipes.count()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
