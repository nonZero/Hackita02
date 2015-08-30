# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_auto_20150830_0506'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectComment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('scope', models.IntegerField(choices=[(1, 'public'), (2, 'private')])),
                ('content', models.TextField(verbose_name='content')),
                ('is_published', models.BooleanField(default=True, verbose_name='is published')),
                ('is_reviewed', models.BooleanField(default=False, verbose_name='is reviewed')),
                ('reviewed_at', models.DateTimeField(verbose_name='reviewed at', null=True)),
                ('in_reply_to', models.ForeignKey(null=True, to='projects.ProjectComment')),
                ('project', models.ForeignKey(to='projects.Project')),
                ('reviewed_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='project_comments_reviewed')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProjectVote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('score', models.IntegerField(choices=[(-1, 'uninterested'), (0, 'neutral'), (1, 'interested'), (2, 'very_interested')])),
                ('project', models.ForeignKey(to='projects.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='projectvote',
            unique_together=set([('user', 'project')]),
        ),
    ]
