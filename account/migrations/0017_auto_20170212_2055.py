# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 20:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_userfollowings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowings',
            name='is_following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_userfollowings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_userfollowings_related', to=settings.AUTH_USER_MODEL),
        ),
    ]