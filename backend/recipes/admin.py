from django.contrib import admin
from recipes.models import (IngredientRecipe, Ingredient, Recipe, ShoppingCart,
                            ShoppingCartIngredient, Tag, TagRecipe,
                            UserRecipe)


class UserRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
    list_editable = (
        'user',
        'recipe'
    )


class ShoppingCartIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'shopping_cart',
        'amount',
    )
    list_editable = (
        'ingredient',
        'shopping_cart',
        'amount',
    )
    fields = (
        'id',
        'ingredient',
        'recipe',
        'amount',
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    list_editable = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )
    list_editable = (
        'name',
        'color',
        'slug'
    )
    list_filter = ('name',)


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tag',
        'recipe'
    )
    list_editable = (
        'tag',
        'recipe'
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_editable = (
        'name',
        'measurement_unit',
    )
    fields = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount',
    )
    list_editable = (
        'ingredient',
        'recipe',
        'amount',
    )
    fields = (
        'id',
        'ingredien',
        'recipe',
        'amount',
    )
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'pub_date',
        'name',
        'text',
        'cooking_time',
    )
    fields = (
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        # 'sum_favorite'
        # 'tags'
    )
    list_editable = (
        'author',
        'name',
        'text',
        'cooking_time',
    )
    list_filter = ('name', 'author', 'tags')
    # list_select_related = ('tags',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ShoppingCartIngredient, ShoppingCartIngredientAdmin)
admin.site.register(UserRecipe, UserRecipeAdmin)
