# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_usernote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernote',
            name='is_open',
            field=models.BooleanField(verbose_name='open'),
        ),
        migrations.AlterField(
            model_name='usernote',
            name='visible_to_user',
            field=models.BooleanField(verbose_name='visible to user', default=False),
        ),
    ]
