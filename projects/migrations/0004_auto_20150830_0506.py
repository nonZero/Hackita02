# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='is published'),
        ),
    ]
