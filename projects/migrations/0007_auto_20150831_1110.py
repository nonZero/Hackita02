# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150830_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcomment',
            name='project',
            field=models.ForeignKey(related_name='comments', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='projectcomment',
            name='scope',
            field=models.IntegerField(choices=[(1, 'public'), (2, 'private')], verbose_name='comment view scope'),
        ),
    ]
