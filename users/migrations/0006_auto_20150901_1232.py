# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0005_auto_20150901_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('group', models.IntegerField(default=0, choices=[(-100, 'negative'), (0, 'neutral'), (100, 'bronze'), (200, 'silver'), (300, 'gold')])),
            ],
            options={
                'ordering': ['-group', 'name'],
            },
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(null=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('operation', models.IntegerField(default=0, choices=[(0, 'Other'), (1, 'Add'), (2, 'Change'), (3, 'Remove')])),
                ('content_type', models.ForeignKey(null=True, to='contenttypes.ContentType')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='logs_created', null=True)),
                ('user', models.ForeignKey(related_name='logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='tags_created', to=settings.AUTH_USER_MODEL)),
                ('tag', models.ForeignKey(related_name='users', to='users.Tag')),
                ('user', models.ForeignKey(related_name='tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usertag',
            unique_together=set([('user', 'tag')]),
        ),
    ]
