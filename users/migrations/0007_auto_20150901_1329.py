# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150901_1232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-group', 'name'], 'verbose_name_plural': 'tags', 'verbose_name': 'tag'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='group',
            field=models.IntegerField(default=0, verbose_name='group', choices=[(-100, 'red'), (0, 'gray'), (100, 'bronze'), (200, 'silver'), (300, 'gold')]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
    ]
