from __future__ import unicode_literals
import copy

from authtools.admin import UserAdmin as UA
from django.contrib import admin

from users import models

class PersonalInfoInline(admin.StackedInline):
    model = models.PersonalInfo

class UserAdmin(UA):
    list_display = (
        'email',
        'hebrew_display_name',
        'english_display_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
    )

    fieldsets = copy.deepcopy(UA.fieldsets)
    fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + (
        'hebrew_display_name',
        'english_display_name',
    )

    inlines = (
        PersonalInfoInline,
    )

    date_hierarchy = "last_login"

admin.site.register(models.User, UserAdmin)
