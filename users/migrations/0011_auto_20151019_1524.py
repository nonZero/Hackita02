# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20151014_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='community_contact_phone',
            field=models.CharField(null=True, blank=True, max_length=120, verbose_name='Phone number (as seen by other community members)', help_text='can be left empty.'),
        ),
        migrations.AddField(
            model_name='user',
            name='community_email',
            field=models.EmailField(null=True, blank=True, max_length=254, verbose_name='Email (as seen by other community members)', help_text='can be left empty.'),
        ),
        migrations.AddField(
            model_name='user',
            name='community_member',
            field=models.BooleanField(verbose_name='community member', default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='community_name',
            field=models.CharField(null=True, blank=True, max_length=120, verbose_name='Hebrew name (as seen by community)'),
        ),
        migrations.AddField(
            model_name='user',
            name='community_personal_info',
            field=models.TextField(null=True, blank=True, verbose_name='Personal info (as seen by other community members)', help_text='Share something about yourself!'),
        ),
    ]
