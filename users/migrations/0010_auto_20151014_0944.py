# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20150908_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernote',
            name='sent_to_user_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
