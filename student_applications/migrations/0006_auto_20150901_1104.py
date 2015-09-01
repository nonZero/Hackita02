# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    Application = apps.get_model("student_applications", "Application")
    # ApplicationStatusLog = apps.get_model("student_applications", "ApplicationStatusLog")
    db_alias = schema_editor.connection.alias

    REGISTERED = 2
    Application.objects.using(db_alias).filter(forms_filled=10).update(
        status=REGISTERED)


class Migration(migrations.Migration):
    dependencies = [
        ('student_applications', '0005_auto_20150901_1103'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
