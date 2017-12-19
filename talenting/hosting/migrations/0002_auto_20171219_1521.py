# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-19 06:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hosting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='hostingreview',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hostingreview',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hostingreview',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hosting.Hosting'),
        ),
        migrations.AddField(
            model_name='hostingrequest',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosting.Hosting'),
        ),
        migrations.AddField(
            model_name='hostingrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hostingphoto',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosting.Hosting'),
        ),
        migrations.AddField(
            model_name='hosting',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
