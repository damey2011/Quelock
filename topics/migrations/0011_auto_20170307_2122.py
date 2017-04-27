# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 21:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0010_topicfollowing'),
        ('account', '__first__')
    ]
    operations = [
        migrations.AlterField(
            model_name='topicfollowing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.UserOtherDetails'),
        ),
    ]
