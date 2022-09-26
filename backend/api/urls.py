from django.urls import include, path
from rest_framework.authtoken import views
from api.views import TagsViewSet
from recipes.models import Tag
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
