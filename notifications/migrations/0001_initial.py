# Generated by Django 2.1.1 on 2018-09-21 01:07

import account.models
import answers.models
import comments.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import messages.models
import notifications.models
import questions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_type', models.PositiveIntegerField(choices=[(1, answers.models.UpVotes), (2, messages.models.ConversationReplies), (3, answers.models.Answer), (4, questions.models.Question), (5, account.models.Reports), (6, answers.models.SuggestEdits), (7, answers.models.Thanks), (8, comments.models.Comment), (9, questions.models.AnswerRequest), (10, notifications.models.UserTurnedOnNotifications), (11, notifications.models.TopicTurnedOnNotifications), (12, questions.models.QuestionFollowing), (13, account.models.UserFollowings)])),
                ('notification_id', models.PositiveIntegerField(default=1)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('read_status', models.BooleanField(default=False)),
                ('actor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actor', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TopicTurnedOnNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_topicturnedonnotifications_subscriber', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_topicturnedonnotifications_topic', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTurnedOnNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_userturnedonnotifications_subscriber', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_userturnedonnotifications_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
