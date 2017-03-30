# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0025_auto_20170307_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('no_of_upvotes', models.IntegerField(default=0, null=True)),
                ('edited', models.IntegerField(default=0, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment')),
                ('writer', models.ForeignKey(null=True, on_delete=models.SET('Anonymous'), to='account.UserOtherDetails')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
