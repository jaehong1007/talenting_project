# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 12:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0002_auto_20171125_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='locationinfo',
            name='place',
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='name',
            new_name='caption',
        ),
        migrations.RemoveField(
            model_name='description',
            name='title',
        ),
        migrations.AddField(
            model_name='description',
            name='exchange',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='description',
            name='neighborhood',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='description',
            name='transportation',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='hosting',
            name='pet',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='hosting',
            name='smoking',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='description',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='description',
            name='to_do',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='hosting',
            name='primary_photo',
            field=models.ImageField(blank=True, default='', upload_to='hosting'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hosting',
            name='summary',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='hosting',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='hostingreview',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='who_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hostingreview',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='who_is_reviewed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hostingreview',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='where_is_reviewed', to='hosting.Hosting'),
        ),
        migrations.DeleteModel(
            name='LocationInfo',
        ),
        migrations.AddField(
            model_name='geolocation',
            name='place',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hosting.Hosting'),
        ),
    ]
