# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 23:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0025_auto_20170307_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_privatemessages_owner_related', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_privatemessages_receiver_related', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_privatemessages_sender_related', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('A', 'Answer'), ('Q', 'Question'), ('U', 'User')], max_length=1)),
                ('type_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userotherdetails',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userotherdetails',
            name='display_picture',
            field=models.ImageField(blank=True, null=True, upload_to='dps'),
        ),
        migrations.AlterField(
            model_name='userotherdetails',
            name='facebook_link',
            field=models.URLField(blank=True, default='http://facebook.com', max_length=100),
        ),
        migrations.AlterField(
            model_name='userotherdetails',
            name='linked_in_profile',
            field=models.URLField(blank=True, default='http://linkedin.com', max_length=100),
        ),
        migrations.AlterField(
            model_name='userotherdetails',
            name='twitter_link',
            field=models.URLField(blank=True, default='http://twitter.com', max_length=100),
        ),
    ]
