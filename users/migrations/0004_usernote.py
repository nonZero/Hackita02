# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150831_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNote',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('visible_to_user', models.BooleanField(default=False)),
                ('content', models.TextField(verbose_name='content')),
                ('sent_to_user_at', models.DateTimeField(null=True)),
                ('is_open', models.BooleanField()),
                ('closed_at', models.DateTimeField(verbose_name='closed at', null=True, blank=True)),
                ('author', models.ForeignKey(related_name='notes_authored', to=settings.AUTH_USER_MODEL)),
                ('closed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='+')),
                ('user', models.ForeignKey(related_name='notes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user note',
                'ordering': ['-created_at'],
                'verbose_name_plural': 'user notes',
            },
        ),
    ]
