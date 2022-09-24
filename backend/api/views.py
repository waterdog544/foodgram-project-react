from api.serializers import TagSerialiser
from recipes.models import Tag
from rest_framework import viewsets

# from djoser.views import UserViewSet

# from backend.api.serializers import CustomUserSerializer, UserSerializer
# from backend.users import User


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return UserListSerializer
#         return UserSerializer

# class CustomUserViewSet(UserViewSet):
#     queryset = User.objects.all()
class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser

