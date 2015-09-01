# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('student_applications', '0006_auto_20150901_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status_changed_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 9, 1, 20, 0, 18, 40902, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
