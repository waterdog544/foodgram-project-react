from recipes.models import Recipe, Ingredient, IngredientRecipe
from users.models import User

user = User.objects.all()
lisa = user[0]
test = user[1]
recipe = Recipe.objects.all()


recipe_j = recipe[1]
recipe_i = recipe[0]
ingredient = Ingredient.objects.all()[1]
print('ingredient: ', ingredient)
print('ingredient.ingredient_recipes: ', ingredient.ingredient_recipes.get(recipe=1).amount)
# print('name lisa: ', lisa)
# print('lisa.favorite_recipes:  ', lisa.favorite_recipes.all())
print('recipe_j.name.: ', recipe_i.name)
print('recipe_j.tags_th.: ', recipe_i.tags_th.all())
# print('recipe.favorite_by_users: ', recipe.favorite_by_users.all())
# print('recipe.favorite_by_users.count: ', recipe.favorite_by_users.count())
# print('recipe.tags: ', recipe.tags.all())
# print('recipe.tags.count: ', recipe.tags.count())
# print('recipe.count_add_favorite:', recipe.added_to_favorite)
# print('name test:', test)
print('subscribe', test.subscribed.all())
print('subscri test:', lisa.is_subscribed(test))
# print('favorite recipes test:', test.is_favorited(recipe_j), recipe_j)
# print('is_in_shopping_cart recipes test:', test.is_in_shopping_cart(recipe_i), recipe_i)
# /^#[0-9A-F]{6}$/i.test('#AABBCC')
# import re
# str = ['#ffffff0', "#ffff00", "#fff0f5"]


# def color_check(str):
#     match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str)
#     if match:                      
#         print('Hex is valid')

#     else:
#         print('Hex is not valid')


# for i in str:
#     color_check(i)