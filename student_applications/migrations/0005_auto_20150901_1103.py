# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student_applications', '0004_auto_20150901_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStatusLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(-1, 'n/a'), (1, 'new (incomplete application)'), (2, 'registered'), (10, 'under discussion'), (11, 'to reject'), (20, 'invite to interview'), (21, 'invited to interview'), (50, 'to accept'), (51, 'accepted'), (100, 'accepted and approved'), (200, 'accepted and declined'), (201, 'rejected')])),
                ('value_changed_at', models.DateTimeField()),
            ],
            options={
                'ordering': ('-value_changed_at',),
            },
        ),
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.IntegerField(default=1, choices=[(-1, 'n/a'), (1, 'new (incomplete application)'), (2, 'registered'), (10, 'under discussion'), (11, 'to reject'), (20, 'invite to interview'), (21, 'invited to interview'), (50, 'to accept'), (51, 'accepted'), (100, 'accepted and approved'), (200, 'accepted and declined'), (201, 'rejected')], verbose_name='status'),
        ),
        migrations.AddField(
            model_name='application',
            name='status_changed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='status_changed_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='+'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='activism_level',
            field=models.IntegerField(null=True, blank=True, choices=[('', 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], verbose_name='involvement in activism'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='availability',
            field=models.IntegerField(null=True, blank=True, choices=[('', 'no answer supplied'), (-1, 'too low'), (0, 'average'), (1, 'high'), (2, 'very high')], verbose_name='present and future availability'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='comm_skills',
            field=models.IntegerField(null=True, blank=True, choices=[('', 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], verbose_name='communication skills'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='comments',
            field=models.TextField(blank=True, verbose_name='review comments', help_text='Consider adding a user note instead '),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='humanism_background',
            field=models.IntegerField(null=True, blank=True, choices=[('', 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], verbose_name='background in humanism'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='overall_impression',
            field=models.IntegerField(help_text='Does the candidate fit the program?', null=True, blank=True, choices=[('', 'no answer supplied'), (-1, 'does not fit'), (0, 'undecided / neutral'), (1, 'fit'), (2, 'highly fits')], verbose_name='overall_impression'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='programming_exp',
            field=models.IntegerField(blank=True, default=None, null=True, choices=[('', 'no answer supplied'), (-1, 'too low'), (0, 'average'), (1, 'high'), (2, 'very high')], verbose_name='programming experience'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='webdev_exp',
            field=models.IntegerField(null=True, blank=True, choices=[('', 'no answer supplied'), (0, 'average'), (1, 'high'), (2, 'very high')], verbose_name='web development experience'),
        ),
        migrations.AddField(
            model_name='applicationstatuslog',
            name='application',
            field=models.ForeignKey(to='student_applications.Application', related_name='status_logs'),
        ),
        migrations.AddField(
            model_name='applicationstatuslog',
            name='value_changed_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='+'),
        ),
    ]
