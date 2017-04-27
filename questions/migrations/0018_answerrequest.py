# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 20:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0017_auto_20170407_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
                ('receipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipient', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
