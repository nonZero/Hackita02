# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_applications', '0009_auto_20150906_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.IntegerField(choices=[(-1, 'n/a'), (1, 'new (incomplete application)'), (2, 'registered'), (5, 'decided not to participate'), (10, 'under discussion'), (11, 'to reject'), (20, 'invite to interview'), (21, 'invited to interview'), (25, 'did not attend interview'), (30, 'participated in interview'), (40, 'to waiting list'), (41, 'waiting list'), (50, 'to accept'), (51, 'accepted'), (100, 'accepted and approved'), (200, 'accepted and declined'), (201, 'rejected')], default=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='applicationstatuslog',
            name='value',
            field=models.IntegerField(choices=[(-1, 'n/a'), (1, 'new (incomplete application)'), (2, 'registered'), (5, 'decided not to participate'), (10, 'under discussion'), (11, 'to reject'), (20, 'invite to interview'), (21, 'invited to interview'), (25, 'did not attend interview'), (30, 'participated in interview'), (40, 'to waiting list'), (41, 'waiting list'), (50, 'to accept'), (51, 'accepted'), (100, 'accepted and approved'), (200, 'accepted and declined'), (201, 'rejected')]),
        ),
    ]
