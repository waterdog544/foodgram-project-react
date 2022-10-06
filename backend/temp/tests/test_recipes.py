import json

from django.db.models import Avg, Max, Min, Sum

from recipes.models import Ingredient, IngredientRecipe, Recipe
from users.models import User

# with open('d:/dev/foodgram-project-react/.vscode/ingredients.json', encoding='utf-8') as f:
#     data = json.load(f)
# for i in data:
#     Ingredient.objects.create(name=i['name'], measurement_unit=i['measurement_unit'])

test = User.objects.get(username='test.user')
ingredients_val = Ingredient.objects.prefetch_related('ingredient_recipes__recipe__shopping_cart_recipes__user').all().filter(ingredient_recipes__recipe__shopping_cart_recipes__user=test).annotate(sum_amount=Sum('ingredient_recipes__amount')).values('name', 'measurement_unit', 'sum_amount')
shopping_list = 'Список продуктов:\n\n'
for i in ingredients_val:
    shopping_list = shopping_list +chr(176) +' ' + i['name'] + ' (' + i['measurement_unit'] + ') - ' + str(i['sum_amount']) + '\n'
print(shopping_list)
user = User.objects.all()
lisa = User.objects.get(username='lisa')

recipe = Recipe.objects.all()
user3 = User.objects.get(username='test3.user')
print('user3:', user3)
try:
    a = user3.subscribers.add(test)
except Exception:
    raise ValueError(Exception)
user3.save()
# print('user3.subscribed.all():', user3.subscribers.all())
# print('user3.subscribed:', user3.subscribed)
# print('user3.subcribers:', user3.subcribers)
print(' test.subscribers.all()', test.subscribers.all())
print(' test.subscribers.all()', test.subscribers.all().order_by('recipes__pub_date').distinct())
print(' recipes__tags_th__slug="breakfast"', test.subscribers.filter(recipes__tags_th__slug = 'Supper').distinct())
# print(' recipes__tag_th__slug="breakfast"', test.subscribers.filter(recipes=2))
recipes = test.shopping_cart_recipes.all()
# select_related(
#             'shopping_cart_recipes__recipes__ingreditnts',
#             'shopping_cart_recipes__recipes__ingreditnts__ingredient',
#         )
ingr = recipes.annotate(ingred_sum = Sum('recipe__ingredients__amount'))
print('recipes', recipes)
print('ingr',ingr)
print('ingr[1].ingred_sum',ingr[1].ingred_sum)
print('ingr[1]',ingr[1].recipe)
print('ingr[2].ingred_sum',ingr[2].ingred_sum)
print('ingr[2]',ingr[2].recipe)
print('lisa.is_subscribed(test2):', lisa.is_subscribed(test))



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