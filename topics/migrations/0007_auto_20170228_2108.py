# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_auto_20170228_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to='topics-dp'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='no_following_topic',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='no_of_questions_under_topic',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
