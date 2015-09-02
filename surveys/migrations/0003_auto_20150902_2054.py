# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20150901_2256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='surveyanswer',
            options={'verbose_name_plural': 'survey answers', 'verbose_name': 'survey answer', 'ordering': ('-is_open', '-answered_at', '-created_at')},
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='is_open',
            field=models.BooleanField(db_index=True, verbose_name='open', default=True),
        ),
    ]
