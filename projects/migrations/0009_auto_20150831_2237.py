# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20150831_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcomment',
            name='user',
            field=models.ForeignKey(related_name='project_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectvote',
            name='user',
            field=models.ForeignKey(related_name='project_votes', to=settings.AUTH_USER_MODEL),
        ),
    ]
