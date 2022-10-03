from django.urls import include, path, re_path
# from rest_framework.authtoken import views
from django.views.decorators.csrf import csrf_exempt
from api.views import (
    FavoriteViewSet,
    TagsViewSet,
    RecipesViewSet,
    IngredientsViewSet,
    # FavoriteCreateAPIView,
    # FavoriteDestroyAPIView
    
    

)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')

router.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    # path(r'recipes/108/favorite', FavoriteCreateAPIView.as_view),
    # re_path(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteCreateAPIView.as_view()),
    # path(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteDestroyAPIView.as_view),

    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
