# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('q13e_slug', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data', django_extensions.db.fields.json.JSONField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='answers')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('user', 'q13e_slug')]),
        ),
    ]
