from django.contrib import admin

from users.models import User


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


admin.site.register(User, UserAdmin)
