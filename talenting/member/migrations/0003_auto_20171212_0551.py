# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20171212_0435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='wish_user',
        ),
        migrations.AddField(
            model_name='user',
            name='wish_profile',
            field=models.ManyToManyField(related_name='wish_profile', to='member.Profile'),
        ),
    ]
