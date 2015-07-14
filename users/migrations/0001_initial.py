# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address', db_index=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active.  Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('hebrew_display_name', models.CharField(max_length=200, verbose_name='display name (Hebrew)', blank=True, null=True)),
                ('english_display_name', models.CharField(max_length=200, verbose_name='display name (English)', blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', verbose_name='groups', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions', related_query_name='user')),
            ],
            options={
                'db_table': 'auth_user',
                'ordering': ('-is_superuser', '-is_staff', '-last_login', 'hebrew_display_name', 'email'),
            },
        ),
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('hebrew_first_name', models.CharField(max_length=200, verbose_name='first name (Hebrew)')),
                ('hebrew_last_name', models.CharField(max_length=200, verbose_name='last name (Hebrew)')),
                ('english_first_name', models.CharField(max_length=200, verbose_name='first name (English)')),
                ('english_last_name', models.CharField(max_length=200, verbose_name='last name (English)')),
                ('main_phone', models.CharField(max_length=50, verbose_name='main phone number')),
                ('alt_phone', models.CharField(max_length=50, verbose_name='alternate phone number', blank=True, null=True)),
                ('city', models.CharField(max_length=200, verbose_name='city', blank=True, null=True)),
                ('address', models.TextField(verbose_name='address', blank=True, help_text='street and number', null=True)),
                ('gender', models.IntegerField(choices=[(1, 'female'), (2, 'male'), (3, 'prefer not to answer')], default=3, verbose_name='gender', help_text='we would like to create a diverse group.')),
                ('skype_username', models.CharField(max_length=100, verbose_name='skype username', blank=True, help_text='optional, for conducting a video interview.', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
