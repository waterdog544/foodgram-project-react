
from rest_framework import authentication, permissions
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status

from api.serializers import (

    IngredientSerializer,

    RecipeSerializer,
    TagSerializer,
    FavoriteSerializer,
    
)
from api.filters import (
    RecipeFilter,
    # RecipeSearch
    )

from rest_framework import mixins


from recipes.models import (
    Ingredient,
    Recipe, Tag,
    UserFavoriteRecipe,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated
)
from api.permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly, IsAdminOrReadOnlyObj
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


# class CustomUserViewSet(UserViewSet):
#     pagination_class = PageNumberPagination


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
class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, IsAdminOrReadOnlyObj)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = RecipeFilter
    search_fields = ('^ingredients_th__name',)
    filterset_fileds = ('tags',)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def create(self, request, pk=None):
        self.tags_add_dict(request=request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        self.tags_add_dict(request=request)
        return self.update(request, *args, **kwargs)

    def tags_add_dict(self, request):
        if 'tags' in request.data:
            tags = request.data.pop('tags', False)
            tags_dict = []
            for tag in tags:
                tags_dict.append({'id': tag})
            request.data['tags'] = tags_dict
        return request


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('favorite_by_users').all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['recipe'] = self.kwargs.get('recipe_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     user = self.request.user
    #     raise ValueError(instance, user)
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def perform_destroy(self, instance):
    #     instance.delete()

# class FavoriteCreateAPIView(generics.DestroyAPIView, generics.CreateAPIView):
#     queryset = Recipe.objects.select_related('favorite_by_users').all()
#     serializer_class = FavoriteSerializer
#     permission_classes = (IsAuthenticated,)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         user = self.request.user
#         raise ValueError(instance, user)
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def perform_destroy(self, instance):
#         instance.delete()


# class FavoriteDestroyAPIView(generics.DestroyAPIView):
#     queryset = Recipe.objects.select_related('favorite_by_users').all()
#     serializer_class = FavoriteSerializer
#     permission_classes = (IsAuthenticated,)
    
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         user = self.request.user
#         raise ValueError(instance, user)
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def perform_destroy(self, instance):
#         instance.delete()

# class FavoriteCreateAPIView(APIView):
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     # @csrf_exempt
#     # @api_view(http_method_names=['POST'])
#     # @csrf_protect
#     # @csrf_exempt
#     # @api_view(http_method_names=['POST'])
#     def post(self, request,):
#         # raise ValueError(request, )
#         try:
#             recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
#         except Exception:
#             raise ValidationError (f'Exception')
#         # Recipe.objects.get(pk=self.kwargs.get('recipe_id'))
#         user = self.request.user
#         # raise ValueError(user, user.id)
#         serializer = FavoriteSerializer(data={'favorite_by_users': user.id})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_serializer(self, *args, **kwargs):
#         """
#         Return the serializer instance that should be used for validating and
#         deserializing input, and for serializing output.
#         """
#         serializer_class = self.get_serializer_class()
#         kwargs['context'] = self.get_serializer_context()
#         return serializer_class(*args, **kwargs)

#     def dispatch(self, request, *args, **kwargs):
#         """
#         `.dispatch()` is pretty much the same as Django's regular dispatch,
#         but with extra hooks for startup, finalize, and exception handling.
#         """
#         self.args = args
#         self.kwargs = kwargs
#         request = self.initialize_request(request, *args, **kwargs)
#         self.request = request
#         self.headers = self.default_response_headers  # deprecate?

#         # try:
#         #     self.initial(request, *args, **kwargs)

#         #     # Get the appropriate handler method
#         #     if request.method.lower() in self.http_method_names:
#         #         handler = getattr(self, request.method.lower(),
#         #                           self.http_method_not_allowed)
#         #     else:
#         #         handler = self.http_method_not_allowed

#         #     response = handler(request, *args, **kwargs)

#         # except Exception as exc:
#         #     response = self.handle_exception(exc)
#         self.initial(request, *args, **kwargs)
#         handler = getattr(self, request.method.lower())
#         response = handler(request, *args)

#         self.response = self.finalize_response(request, response, *args, **kwargs)
#         return self.response

        
#     #     recipe.favorite_by_users.add(user)
#     # def Response(serializer.data, status=status.HTTP_201_CREATED)


