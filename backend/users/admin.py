from django.contrib import admin

from users.models import Subscriptions, User


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'follower',
    )
    list_editable = (
        'author',
        'follower',
    )
    fields = (
        'author',
        'follower',
    )
    search_fields = (
        'author',
        'follower',
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'username',
        'password',
    )
    list_filter = ('email', 'first_name')
    list_editable = (
        'email',
        'first_name',
        'last_name',
        'username',
        'password',
    )
    empty_value_display = '-пусто-'
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_superuser')


admin.site.register(User, UserAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
