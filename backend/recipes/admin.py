from django.contrib import admin

from recipes.models import (Ingredient, IngredientRecipe, Recipe,
                            ShoppingCartRecipe, Tag, TagRecipe,
                            UserFavoriteRecipe)


class UserFavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
    list_editable = (
        'user',
        'recipe'
    )


# class ShoppingCartIngredientAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'ingredient',
#         'shopping_cart',
#         'amount',
#     )
#     list_editable = (
#         'ingredient',
#         'shopping_cart',
#         'amount',
#     )
#     fields = (
#         'id',
#         'ingredient',
#         'recipe',
#         'amount',
#     )


# # class ShoppingCartIngredientInline(admin.TabularInline):
# #     model = ShoppingCartIngredient.ingredient.through


class ShoppingCartRecipeAdmin(admin.ModelAdmin):
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
    fields = (
        'user',
        'recipe',
        # 'ingredients',
        # 'amount'
    )
    # filter_horizontal = ('ingredient',)
    # inlines = (ShoppingCartIngredientInline,)


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
    search_fields = ('name',)


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
        'ingredient',
        'recipe',
        'amount',
    )
    empty_value_display = '-пусто-'


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients_th.through


class TagInline(admin.TabularInline):
    model = Recipe.tags_th.through


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'pub_date',
        'name',
        'text',
        'cooking_time',
        'added_to_favorite'
    )
    fields = (
        'author',
        'name',
        'image',
        'image_tag',
        'text',
        'cooking_time',
        'added_to_favorite'
    )
    readonly_fields = ('image_tag', 'added_to_favorite')
    inlines = (
        IngredientInline,
        TagInline,)
    list_editable = (
        'author',
        'name',
        'text',
        'cooking_time',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCartRecipe, ShoppingCartRecipeAdmin)
admin.site.register(UserFavoriteRecipe, UserFavoriteRecipeAdmin)
