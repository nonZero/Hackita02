from __future__ import unicode_literals

from authtools.admin import UserAdmin
from django.contrib import admin

from users import models


class UserAdmin(UserAdmin):
    list_display = (
        'email',
        'hebrew_display_name',
        'english_display_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
    )

    date_hierarchy = "last_login"


admin.site.register(models.User, UserAdmin)
