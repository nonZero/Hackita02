from django.contrib import admin

from hackita02.html import HTMLWidget, HTMLField

from surveys import models


class SurveyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        HTMLField: {'widget': HTMLWidget()},
    }


admin.site.register(models.Survey, SurveyAdmin)
admin.site.register(models.SurveyAnswer)
