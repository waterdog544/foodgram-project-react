from django.contrib import admin
from recipes.models import (IngredienRecipe, Ingredient, Recipe, ShoppingCart,
                            ShoppingCartIngredient, Subscribe, Tag, TagRecipe,
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


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'subscriber'
    )
    list_editable = (
        'author',
        'subscriber'
    )


class ShoppingCartIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredien',
        'shopping_cart',
        'amount',
    )
    list_editable = (
        'ingredien',
        'shopping_cart',
        'amount',
    )
    fields = (
        'id',
        'ingredien',
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
        'name',
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
        'id',
        'tag',
        'recipe'
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredien',
        'recipe',
        'amount',
    )
    list_editable = (
        'ingredien',
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
        'tags',
    )
    fields = (
        'id',
        'author',
        'pub_date',
        'name',
        'image',
        'text',
        'cooking_time',
        'tags',
        'sum_favorite'
    )
    list_editable = (
        'author',
        'pub_date',
        'name',
        'text',
        'cooking_time',
        'tags',
    )
    list_filter = ('name', 'author', 'recipe__tags')
    list_select_related = ('tags',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredienRecipe, IngredientRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ShoppingCartIngredient, ShoppingCartIngredientAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(UserRecipe, UserRecipeAdmin)
