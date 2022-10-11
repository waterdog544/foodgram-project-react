# Generated by Django 3.2.15 on 2022-10-11 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavoriterecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='tagrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='tagrecipe',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.tag', verbose_name='Тэг'),
        ),
        migrations.AddField(
            model_name='tag',
            name='recipes',
            field=models.ManyToManyField(blank=True, through='recipes.TagRecipe', to='recipes.Recipe', verbose_name='Рецепты'),
        ),
        migrations.AddField(
            model_name='shoppingcartrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_recipes', to='recipes.recipe', verbose_name='Рецепт в корзине'),
        ),
        migrations.AddField(
            model_name='shoppingcartrecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Корзина пользователя'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='favorite_by_users',
            field=models.ManyToManyField(blank=True, through='recipes.UserFavoriteRecipe', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи, добавившие рецепт в избранное'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients_th',
            field=models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag_through',
            field=models.ManyToManyField(through='recipes.TagRecipe', to='recipes.Tag', verbose_name='Тэги'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipes', to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipes',
            field=models.ManyToManyField(blank=True, through='recipes.IngredientRecipe', to='recipes.Recipe', verbose_name='Рецепты'),
        ),
        migrations.AddConstraint(
            model_name='userfavoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe'),
        ),
        migrations.AddConstraint(
            model_name='tagrecipe',
            constraint=models.UniqueConstraint(fields=('tag', 'recipe'), name='unique_tag_recipe'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('name', 'slug'), name='unique_name_slug'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('author', 'name'), name='unique_author_name'),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient_recipe'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement_unit'),
        ),
    ]
