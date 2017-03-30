from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from account.serializers import UserSerializer, UserOtherDetailsSerializer
from answers.models import Answer
from questions.serializers import QuestionSerializer


class AnswerSerializer(ModelSerializer):
    writer = UserOtherDetailsSerializer(read_only=True)
    question = QuestionSerializer()
    no_of_comments = SerializerMethodField()
    upvoted = SerializerMethodField()
    downvoted = SerializerMethodField()
    archived = SerializerMethodField()
    thanked = SerializerMethodField()
    edit_suggested = SerializerMethodField()

    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'writer',
            'date_written',
            'time_written',
            'body',
            'no_of_upvotes',
            'no_of_downvotes',
            'no_of_views',
            'no_of_comments',
            'upvoted',
            'downvoted',
            'archived',
            'thanked',
            'edit_suggested',
            'anonymous'
        ]

    def get_no_of_comments(self, obj):
        try:
            return obj.getComments()
        except:
            return 0

    def get_upvoted(self, obj):
        try:
            return obj.isUpvoted(self.context.get('request').user)
        except:
            return False

    def get_downvoted(self, obj):
        try:
            return obj.isDownvoted(self.context.get('request').user)
        except:
            return False

    def get_archived(self, obj):
        try:
            return obj.isArchived(self.context.get('request').user)
        except:
            return False

    def get_thanked(self, obj):
        try:
            return obj.hasThanked(self.context.get('request').user)
        except:
            return False

    def get_edit_suggested(self, obj):
        try:
            return obj.hasSuggested(self.context.get('request').user)
        except:
            return False


class BookmarkSerializer(ModelSerializer):
    answer = AnswerSerializer(read_only=True)

    class Meta:
        user = User
        fields = '__all__'
