# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0014_auto_20170213_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=models.SET('Anonymous'), to='account.UserOtherDetails'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(on_delete=models.SET('Anonymous'), to='answers.Answer'),
        ),
    ]
