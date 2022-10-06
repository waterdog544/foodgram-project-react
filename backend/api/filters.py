import django_filters
from recipes.models import Recipe
from users.models import User
from rest_framework.serializers import ValidationError


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags_th__slug')

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
        elif is_favorited:
            return parent.filter(favorite_by_users=user)
        elif is_in_shopping_cart:
            return parent.filter(shopping_cart_recipes__user=user)
        return parent

    def get_check_values(self, name: str) -> int:
        obj = getattr(self.request, 'GET', None).get(name)
        if obj is None:
            return None
        try:
            obj_int = int(obj)
        except Exception as e:
            mess = {'errors': (
                f'{e}. Значение параметра {name} = {obj},'
                f' должно быть: (0, 1).'
            )}
            raise ValidationError(mess)
        if obj_int in (0, 1):
            return obj_int
        elif obj:
            mess = {'errors': f'Value Error. Значение параметра {name} = {obj}, должно быть: (0, 1).'}
            raise ValidationError(mess)



class SubsciptionsFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = []
    
    @property
    def qs(self):
        parent = super().qs
        tags = self.request.GET.get('tags')
        if tags:
            return parent.filter(
                recipes__tags_th__slug=tags
            ).order_by('-recipes__pub_date').distinct()
        return parent.order_by('-recipes__pub_date').distinct()
        
        # for postgres
        # if tags:
        #     return parent.filter(
        #         recipes__tags_th__slug=tags
        #     ).order_by('recipes__pub_date').distinct(
        #         'recipes__tags_th__slug', 'recipes__pub_date'
        #     )
        # return parent.order_by(
        #     'recipes__pub_date'
        #     ).distinct('recipes__pub_date')


