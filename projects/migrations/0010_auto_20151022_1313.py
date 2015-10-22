# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0009_auto_20150831_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectBid',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('value', models.IntegerField()),
                ('project', models.ForeignKey(related_name='bids', to='projects.Project')),
                ('user', models.ForeignKey(related_name='project_bids', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'project bids',
                'ordering': ['-created_at'],
                'verbose_name': 'project bid',
            },
        ),
        migrations.AlterUniqueTogether(
            name='projectbid',
            unique_together=set([('user', 'project')]),
        ),
    ]
