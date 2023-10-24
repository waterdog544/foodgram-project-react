import django_filters
from rest_framework import filters
from rest_framework.serializers import ValidationError

from recipes.models import Recipe, Tag


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__tag__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('tags',)

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        is_favorited = self.get_check_values('is_favorited')
        is_in_shopping_cart = self.get_check_values('is_in_shopping_cart')
        if is_favorited and is_in_shopping_cart:
            return parent.filter(
                favorite_by_users=user
            ).filter(shopping_cart_recipes__user=user)
        if is_favorited:
            return parent.filter(favorite_by_users=user)
        if is_in_shopping_cart:
            return parent.filter(shopping_cart_recipes__user=user)
        return parent

    def get_check_values(self, name: str) -> int:
        obj = self.request.GET.get(name)
        if obj is None:
            return None
        try:
            obj_int = int(obj)
        except Exception:
            mess = {'errors': (
                f'Значение параметра {name} = {obj},'
                f' должно быть: (0, 1).'
            )}
            raise ValidationError(mess)
        if obj_int in (0, 1):
            return obj_int
        if obj:
            mess = mess
            raise ValidationError(mess)
        return None
