# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_topicfollowing'),
    ]

    operations = [
        migrations.AddField(
            model_name='userotherdetails',
            name='bio',
            field=models.TextField(null=True),
        ),
    ]
