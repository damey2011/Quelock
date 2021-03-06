# Generated by Django 2.1.1 on 2018-09-21 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlreadyReadAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('A', 'Answer'), ('Q', 'Question'), ('U', 'User')], max_length=1)),
                ('type_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserFigures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.PositiveIntegerField(default=0)),
                ('answer_views', models.PositiveIntegerField(default=0)),
                ('questions', models.PositiveIntegerField(default=0)),
                ('question_views', models.PositiveIntegerField(default=0)),
                ('followers', models.PositiveIntegerField(default=0)),
                ('followings', models.PositiveIntegerField(default=0)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('thanks', models.PositiveIntegerField(default=0)),
                ('comments', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserOtherDetails',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('answer_no_of_views', models.IntegerField(default=0, null=True)),
                ('display_picture', models.ImageField(blank=True, default='/default/user.png', null=True, upload_to='dps')),
                ('bio', models.TextField(blank=True, default='NA', null=True)),
                ('college', models.CharField(blank=True, default='NA', max_length=50)),
                ('works', models.CharField(blank=True, default='NA', max_length=100)),
                ('lives', models.CharField(blank=True, default='NA', max_length=50)),
                ('followers', models.IntegerField(default=0)),
                ('following', models.IntegerField(default=0)),
                ('facebook_link', models.URLField(blank=True, default='http://facebook.com', max_length=100)),
                ('twitter_link', models.URLField(blank=True, default='http://twitter.com', max_length=100)),
                ('linked_in_profile', models.URLField(blank=True, default='http://linkedin.com', max_length=100)),
                ('no_of_questions', models.IntegerField(default=0)),
                ('no_of_answers', models.IntegerField(default=0)),
                ('most_active_topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='topics.Topic')),
            ],
        ),
        migrations.AddField(
            model_name='userfollowings',
            name='is_following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_userfollowings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userfollowings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_userfollowings_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userfigures',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
