# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student_applications', '0003_auto_20150725_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationReview',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('last_edited_at', models.DateTimeField(verbose_name='last edited at', auto_now_add=True)),
                ('programming_exp', models.IntegerField(verbose_name='programming experience', blank=True, choices=[(None, 'no answer supplied'), (-1, 'too low'), (0, 'average'), (1, 'high'), (2, 'very high')], null=True)),
                ('webdev_exp', models.IntegerField(verbose_name='web development experience', blank=True, choices=[(None, 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], null=True)),
                ('activism_level', models.IntegerField(verbose_name='involvement in activism', blank=True, choices=[(None, 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], null=True)),
                ('availability', models.IntegerField(verbose_name='present and future availability', blank=True, choices=[(None, 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], null=True)),
                ('humanism_background', models.IntegerField(verbose_name='background in humanism', blank=True, choices=[(None, 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], null=True)),
                ('comm_skills', models.IntegerField(verbose_name='communication skills', blank=True, choices=[(None, 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], null=True)),
                ('overall_impression', models.IntegerField(verbose_name='overall_impression', blank=True, choices=[(None, 'no answer supplied'), (-1, 'does not fit'), (0, 'undecided / neutral'), (1, 'fit'), (2, 'highly fits')], null=True, help_text='Does the candidate fit the program?')),
                ('comments', models.TextField(verbose_name='review comments', help_text='Consider adding a user note instead ')),
                ('application', models.ForeignKey(to='student_applications.Application', related_name='reviews')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='application_reviews')),
            ],
            options={
                'verbose_name': 'application review',
                'ordering': ('-created_at',),
                'verbose_name_plural': 'application reviews',
            },
        ),
        migrations.AlterUniqueTogether(
            name='applicationreview',
            unique_together=set([('application', 'user')]),
        ),
    ]
