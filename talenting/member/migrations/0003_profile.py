# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 05:16
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20171124_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('self_intro', models.TextField()),
                ('my_talent', models.TextField()),
                ('city', models.CharField(max_length=20)),
                ('occupation', models.CharField(max_length=20)),
                ('available_languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), size=None)),
                ('profile_image', models.ImageField(upload_to='profile')),
            ],
        ),
    ]
