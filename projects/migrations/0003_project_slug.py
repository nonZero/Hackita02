# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.CharField(verbose_name='slug', max_length=100, unique=True, null=True),
        ),
    ]
