# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import users.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=400, verbose_name='title')),
                ('slug', models.SlugField()),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_open', models.BooleanField(default=True, verbose_name='invitations open')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('starts_at', models.DateTimeField(verbose_name='starts at')),
                ('ends_at', models.DateTimeField(verbose_name='ends at')),
                ('registration_ends_at', models.DateTimeField(verbose_name='registartion ends at', null=True, blank=True)),
                ('location', models.CharField(max_length=400, verbose_name='location', null=True)),
                ('description', models.TextField(null=True)),
                ('created_by', models.ForeignKey(related_name='events_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventInvitation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('slug', models.SlugField(default=users.models.generate_code)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'New invitation'), (2, 'Invitation sent'), (3, 'Invitation approved'), (4, 'Invitation maybe'), (5, 'Invitation declined')], verbose_name='Status')),
                ('note', models.TextField(verbose_name='Note', null=True, blank=True)),
                ('attendance', models.IntegerField(blank=True, choices=[(1, 'Attended'), (2, 'Partially attended'), (3, 'Did not attend')], null=True, verbose_name='Attendance')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='event_invitations_created')),
                ('event', models.ForeignKey(related_name='invitations', to='events.Event')),
                ('user', models.ForeignKey(related_name='invitations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['event', 'status', 'created_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='eventinvitation',
            unique_together=set([('event', 'user')]),
        ),
    ]
