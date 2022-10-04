from django.urls import include, path, re_path
# from rest_framework.authtoken import views
from django.views.decorators.csrf import csrf_exempt
from api.views import (
    # FavoriteViewSet,
    SubscriptionsViewSet,
    TagsViewSet,
    RecipesViewSet,
    IngredientsViewSet,

    # FavoriteCreateAPIView,
    # FavoriteDestroyAPIView
    favorite_set,
    subscribe_set
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'users/subsciptions', SubscriptionsViewSet, basename='subsciptions')


urlpatterns = [
    re_path(r'recipes/(?P<recipe_id>\d+)/favorite', favorite_set),
    re_path(r'users/(?P<user_id>\d+)/subscribe', subscribe_set),
    
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
