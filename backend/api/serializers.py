# from rest_framework.serializers import ValidationError
# import webcolors
import re
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Tag
from rest_framework import serializers
from users.models import User



class TagSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

    def validate_color(self, value):
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
        if not match:
            raise serializers.ValidationError(
                'Строка не соответсвует HEX-формату'
            )
        return value


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return obj.is_subscribed(self.context['request'].user)
    

# class Hex2NameColor(serializers.Field):
#     def to_representation(self, value):
#         return value

#     def to_internal_value(self, data):
#         try:
#             webcolors.hex_to_name(data)
#         except ValueError:
#             raise serializers.ValidationError('Цвета нет в библиотеке')
#         return data
