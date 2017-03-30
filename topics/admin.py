from django.contrib import admin

from topics.models import Topic, TopicFollowing

admin.site.register(Topic)
admin.site.register(TopicFollowing)

