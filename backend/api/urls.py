from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientsViewSet, RecipesViewSet, ShoppingCartViewSet,
                       SubscriptionsViewSet, TagsViewSet, favorite_set,
                       shopping_cart_set, shopping_cart_get, subscribe_set)

router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(
    r'users/subsciptions', SubscriptionsViewSet, basename='subsciptions'
)
# router.register(
#     r'recipes/download_shopping_cart',
#     ShoppingCartViewSet,
# #     basename='shopping_cart'
# )


urlpatterns = [
    re_path(r'recipes/(?P<recipe_id>\d+)/shopping_cart', shopping_cart_set),
    re_path(r'recipes/download_shopping_cart', shopping_cart_get),
    re_path(r'recipes/(?P<recipe_id>\d+)/favorite', favorite_set),
    re_path(r'users/(?P<user_id>\d+)/subscribe', subscribe_set),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
