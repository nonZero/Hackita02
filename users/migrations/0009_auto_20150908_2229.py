# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    User = apps.get_model("users", "User")
    db_alias = schema_editor.connection.alias

    User.objects.using(db_alias).filter(is_staff=True).update(team_member=True)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0008_user_team_member'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
