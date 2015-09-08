# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150901_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='team_member',
            field=models.BooleanField(verbose_name='team member', default=False),
        ),
    ]
