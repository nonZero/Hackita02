from __future__ import unicode_literals

from authtools.admin import NamedUserAdmin
from django.contrib import admin

from users import models


class LMSUserAdmin(NamedUserAdmin):
    list_display = (
        'name',
        'is_active',
        'email',
        'is_staff',
        'is_superuser',
        'last_login',
    )

    date_hierarchy = "last_login"


admin.site.register(models.User, LMSUserAdmin)
