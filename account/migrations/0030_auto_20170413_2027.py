# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_auto_20170407_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userotherdetails',
            name='bio',
            field=models.TextField(blank=True, default='NA', null=True),
        ),
        migrations.AlterField(
            model_name='userotherdetails',
            name='display_picture',
            field=models.ImageField(blank=True, default='/default/user.png', null=True, upload_to='dps'),
        ),
    ]
