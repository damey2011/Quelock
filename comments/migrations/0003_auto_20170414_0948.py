# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 09:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_parent_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=models.SET('Anonymous'), to=settings.AUTH_USER_MODEL),
        ),
    ]
