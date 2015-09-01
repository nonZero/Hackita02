# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hackita02.html
from django.conf import settings
import django_extensions.db.fields.json
import users.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email_subject', models.CharField(max_length=250)),
                ('email_content', hackita02.html.HTMLField(blank=True, null=True)),
                ('q13e', models.TextField()),
            ],
            options={
                'verbose_name': 'survey',
                'verbose_name_plural': 'surveys',
            },
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(default=users.models.generate_code)),
                ('answered_at', models.DateTimeField(blank=True, null=True)),
                ('data', django_extensions.db.fields.json.JSONField(blank=True, null=True)),
                ('survey', models.ForeignKey(to='surveys.Survey', related_name='answers')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='survey_answers')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='surveyanswer',
            unique_together=set([('survey', 'user')]),
        ),
    ]
