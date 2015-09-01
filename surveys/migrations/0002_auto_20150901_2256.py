# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hackita02.html


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='email_content',
            field=hackita02.html.HTMLField(verbose_name='email content', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='email_subject',
            field=models.CharField(max_length=250, verbose_name='email subject'),
        ),
    ]
