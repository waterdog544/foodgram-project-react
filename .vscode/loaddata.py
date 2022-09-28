import json
from recipes.models import Ingredient

with open('ingredients.json', encoding='utf-8') as f:
    data = json.load(f)
for i in data:
    Ingredient.objects.create(name=i['name'], measurement_unit=i['measurement_unit'])
