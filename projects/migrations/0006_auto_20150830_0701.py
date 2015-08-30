# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20150830_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectvote',
            name='project',
            field=models.ForeignKey(to='projects.Project', related_name='votes'),
        ),
        migrations.AlterField(
            model_name='projectvote',
            name='score',
            field=models.IntegerField(choices=[(-1, 'uninterested'), (0, 'neutral'), (1, 'interested'), (2, 'very interested')]),
        ),
    ]
