from rest_framework.response import Response
from rest_framework import status
from functools import partial
from api.serializers import (
    IngredientSerializer,
    # RecipeReadSerializer,
    RecipeSerializer,
    RecipeNewSerializer,
    RecipeNew1Serializer,
    TagSerializer,
)

from recipes.models import (
    Ingredient,
    Recipe, Tag,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
)
from api.permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly


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
    permission_classes = (IsAdminOrReadOnly,)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    serializer_class = RecipeNew1Serializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    # def get_serializer_class(self):
    #     # if self.action == 'create':
    #     # #     raise ValidationError(
    #     # #     f' {self.action} Необходимо добавить tag'
    #     # # )
    #     #     return RecipeNewSerializer
    #     # return RecipeSerializer
    #     return RecipeNew1Serializer

    # def perform_create(self, serializer):
    #     print(serializer.data)
    #     raise ValidationError(
    #         f' SELF {self} ACTION {self.action} INITIAL {serializer.initial_data["tags"]}'
    #         f' SERIALIZER{serializer}Необходимо добавить tag'
    #         f' DATA {serializer.data.get("tags")}'
    #     )
    #     return super().perform_create(serializer)
    
    def create(self, request, pk=None):
        try:
            tags = request.data.pop('tags')
        except Exception:
            raise ValidationError(
                'tags - обязательное поле. Необходимо добавить тэг.'
            )
        # tags = request.data.pop('tags')
        tags_dict = []
        for tag in tags:
            tags_dict.append({'tag': tag})
        request.data['tags'] = tags_dict
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    # def partial_update(self, request, pk=None):
    #     if tags in request.data:
    #         tags = request.data.pop('tags')
    #         tags_dict = []
    #         for tag in tags:
    #             tags_dict.append({'id': tag})
    #         request.data['tags'] = tags_dict
    #     recipe = self.get_object            
    #     serializer = RecipeSerializer(data=request.data,)
    #     if serializer.is_valid():

    #     raise ValidationError(
    #         f' SELF {request.data} '
    #         # f'ACTION {self.action} INITIAL {serializer.initial_data["tags"]}'
            # )
        # serialized = DemoSerializer(request.user, data=request.data, partial=True)
        # return Response(status=status.HTTP_202_ACCEPTED)
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = UserFavoriteRecipe.objects.select_related('recipe').all()
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer
		
		"<rest_framework.request.Request: DELETE '/api/recipes/110/favorite/'>"
		
	class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('favorite_by_users').all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('post', 'delete')

    def create(self, request, *args, **kwargs):
        # raise ValidationError (self.request)
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
    
    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     `.dispatch()` is pretty much the same as Django's regular dispatch,
    #     but with extra hooks for startup, finalize, and exception handling.
    #     """
    #     self.args = args
    #     self.kwargs = kwargs
    #     request = self.initialize_request(request, *args, **kwargs)
    #     self.request = request
    #     self.headers = self.default_response_headers  # deprecate?

        # try:
        #     self.initial(request, *args, **kwargs)

        #     # Get the appropriate handler method
        #     if request.method.lower() in self.http_method_names:
        handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
        #     else:
        #         handler = self.http_method_not_allowed

        #     response = handler(request, *args, **kwargs)

        # except Exception as exc:
        # if request.method.lower() in self.http_method_names:
        #     response = handler(request, *args, **kwargs)
        #     response = self.handle_exception(exc)
        # self.initial(request, *args, **kwargs)
        # handler = getattr(self, request.method.lower())
        # response = handler(request, *args)

        # self.response = self.finalize_response(request, response, *args, **kwargs)
        # return self.response


    # def dispatch(self, request, *args, **kwargs):
    #     # Try to dispatch to the right method; if a method doesn't exist,
    #     # defer to the error handler. Also defer to the error handler if the
    #     # request method isn't on the approved list.
    #     # if request.method.lower() in self.http_method_names:
    #     handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    #     # else:
    #     #     handler = self.http_method_not_allowed
    #     return handler(request, *args, **kwargs)

    # def http_method_not_allowed(self, request, *args, **kwargs):
    #     logger.warning(
    #         'Method Not Allowed (%s): %s', request.method, request.path,
    #         extra={'status_code': 405, 'request': request}
    #     )
    #     return HttpResponseNotAllowed(self._allowed_methods())

    # @action(detail=True, methods=('post',))
    # def dispatch(self, request, *args, **kwargs):
    #     raise ValueError 
    #     return super().dispatch(request, *args)
    #    @action(detail=True, methods=('post',))
    # @action(detail=False, methods=('delete',))
    # @api_view
    # @csrf_exempt

    # def initial(self, request, *args, **kwargs):
    #     if request.method.lower()=='delete':
    #     #     raise ValidationError(f"Req {request} kwargs {self.kwargs}")
    #         self.kwargs = self.get_parser_context(request).get('kwargs')
    #     return super().initial(request, *args, **kwargs)
    # # def initial(self, request, *args, **kwargs):
    # #     # if request.method.lower()=='delete':
    # #     #     raise ValidationError(f"Req {request} kwargs {self.kwargs}")
    # #     #     self.kwargs = self.get_parser_context(request).get('kwargs')
    # #     raise ValidationError(f"{self.get_parser_context(request).get('kwargs')}")
    #     # raise ValueError(request)

    #     # return super().initial(request, *args, **kwargs)
    
    def initialize_request(self, request, *args, **kwargs):
        # raise ValidationError(f"TEST {request}")
        if request.method.lower() ==' delete':
            self.kwargs = self.get_parser_context(request).get('kwargs')
            raise ValidationError(f"TEST {request}")
            return super().initialize_request(request, *args, self.kwargs)
        return super().initialize_request(request, *args, **kwargs)
        # raise ValidationError(f"TEST {request}")
        parser_context = self.get_parser_context(request)
        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

    
    def destroy(self, request, *args, **kwargs):
        # raise ValueError(kwargs.get('recipe_id'))
        # instance = self.get_object()
        instance = Recipe.objects.get(pk=kwargs.get('recipe_id'))
        user = self.request.user
        # raise ValueError(instance, user)
        instance.favorite_by_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    # def perform_destroy(self, instance):
        instance.delete()

class FavoriteCreateAPIView(generics.DestroyAPIView, generics.CreateAPIView):
    queryset = Recipe.objects.select_related('favorite_by_users').all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        raise ValueError(instance, user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class FavoriteDestroyAPIView(generics.DestroyAPIView):
    queryset = Recipe.objects.select_related('favorite_by_users').all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        raise ValueError(instance, user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class FavoriteCreateAPIView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # @csrf_exempt
    # @api_view(http_method_names=['POST'])
    # @csrf_protect
    # @csrf_exempt
    # @api_view(http_method_names=['POST'])
    def post(self, request,):
        # raise ValueError(request, )
        try:
            recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        except Exception:
            raise ValidationError (f'Exception')
        # Recipe.objects.get(pk=self.kwargs.get('recipe_id'))
        user = self.request.user
        # raise ValueError(user, user.id)
        serializer = FavoriteSerializer(data={'favorite_by_users': user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        # try:
        #     self.initial(request, *args, **kwargs)

        #     # Get the appropriate handler method
        #     if request.method.lower() in self.http_method_names:
        #         handler = getattr(self, request.method.lower(),
        #                           self.http_method_not_allowed)
        #     else:
        #         handler = self.http_method_not_allowed

        #     response = handler(request, *args, **kwargs)

        # except Exception as exc:
        #     response = self.handle_exception(exc)
        self.initial(request, *args, **kwargs)
        handler = getattr(self, request.method.lower())
        response = handler(request, *args)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

        
    #     recipe.favorite_by_users.add(user)
    # def Response(serializer.data, status=status.HTTP_201_CREATED)
