from rest_framework import serializers
from answers.models import UpVotes, Answer
from answers.serializers import AnswerSerializer


class FeedItemSerializer(serializers.Serializer):
    feed_type = serializers.CharField(max_length=20)
    data = serializers.CharField(max_length=100000)


class UpvotedAnswersSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = UpVotes
        fields = [
            'answer'
        ]


class FeedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'writer',
            'date_written',
            'time_written',
            'body',
            'no_of_upvotes',
            'no_of_views',
            'no_of_comments',
            'anonymous'
        ]
