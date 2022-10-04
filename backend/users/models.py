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
    # subscribed = models.ForeignKey(
    #     'self',
    #     blank=True,
    #     related_name = 'subscribers'
    # )
    subscribers = models.ManyToManyField(
        'self',
        blank=True,
        related_name='subscribed',
        verbose_name='Подписки на авторов'
    )

    def __str__(self):
        return self.username

    def is_subscribed(self, anyuser):
        return self.subscribers.filter(id=anyuser.id).exists()
    
    @property
    def recipes_count(self):
        return self.recipes.count()

    # def is_favorited(self, anyrecipe):
    #     return self.favorite_recipes.filter(id=anyrecipe.id).exists()
    
    # def is_in_shopping_cart(self, anyrecipe):
    #     return self.shopping_cart_recipes.filter(id=anyrecipe.id).exists()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# class Subscriptions(models.Model):
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name='Автор'
#     )
#     subscriber = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         # related_name='subscribers',
#         verbose_name='Подписчик'
#     )

    # def __str__(self):
    #     return f'{self.subscriber} на {self.author} '

    # class Meta:
    #     verbose_name = 'Подписка'
    #     verbose_name_plural = 'Подписки'
    #     constraints = (
    #         models.UniqueConstraint(
    #             fields=('author', 'subscriber'),
    #             name='unique_author_subscriber'
    #         ),
    #     )
    