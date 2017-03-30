from rest_framework import serializers
from account.serializers import UserOtherDetailsSerializer

from topics.models import Topic, TopicFollowing


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TopicFollowingSerializer(serializers.ModelSerializer):
    user = UserOtherDetailsSerializer(read_only=True)

    class Meta:
        model = TopicFollowing
        fields = ['user']
