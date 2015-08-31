# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20150831_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name_plural': 'projects', 'verbose_name': 'project', 'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='projectcomment',
            options={'verbose_name_plural': 'project comments', 'verbose_name': 'project comment', 'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='projectcomment',
            name='in_reply_to',
            field=models.ForeignKey(to='projects.ProjectComment', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projectcomment',
            name='reviewed_at',
            field=models.DateTimeField(verbose_name='reviewed at', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projectcomment',
            name='reviewed_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='project_comments_reviewed'),
        ),
    ]
