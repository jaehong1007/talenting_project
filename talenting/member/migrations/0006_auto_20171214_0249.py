# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_auto_20171213_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileimage',
            name='image',
            field=models.ImageField(max_length=255, upload_to='profile'),
        ),
    ]
