# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import migrations

logger = logging.getLogger(__name__)


def fix_user(u):
    u.community_member = True
    try:
        u.community_name = "{} {}".format(
            u.personalinfo.hebrew_first_name,
            u.personalinfo.hebrew_last_name,
        )
        u.community_contact_phone = u.personalinfo.main_phone
    except Exception as e:
        assert "User has no personalinfo" in str(e)
        u.community_name = u.hebrew_display_name

    u.community_email = u.email
    u.save()
    logger.info('fixed user {}'.format(u.email))


def import_community_info(apps, schema_editor):
    User = apps.get_model("users", "User")

    qs = User.objects.filter(team_member=True)
    for u in qs:
        fix_user(u)

    ACCEPTED_AND_APPROVED = 100
    qs = User.objects.filter(application__status=ACCEPTED_AND_APPROVED)
    for u in qs:
        fix_user(u)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0011_auto_20151019_1524'),
    ]

    operations = [
        migrations.RunPython(import_community_info)
    ]
