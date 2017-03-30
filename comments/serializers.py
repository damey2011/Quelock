from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from account.serializers import UserOtherDetailsSerializer
from answers.models import Answer
from comments.models import Comment


class CommentDetailsSerializer(ModelSerializer):
    writer = UserOtherDetailsSerializer(read_only=True)
    parent_answer = SerializerMethodField()
    replies = HyperlinkedIdentityField(view_name='children_comment')
    replies_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'writer',
            'body',
            'no_of_upvotes',
            'timestamp',
            'replies',
            'replies_count',
            'parent_answer',
        ]
        read_only_fields = [
            'no_of_upvotes',
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_parent_answer(self, obj):
        if obj.parent_answer is not None:
            return CommentParentAnswerSerializer(obj.parent_answer).data
        return None


class CommentChildSerializer(ModelSerializer):
    writer = UserOtherDetailsSerializer(read_only=True)
    replies = HyperlinkedIdentityField(view_name='children_comment')
    replies_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'writer',
            'body',
            'no_of_upvotes',
            'parent',
            'replies',
            'replies_count'
        ]

        read_only_fields = [
            'no_of_upvotes'
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_replies_count(self, obj):
        try:
            return obj.children().count()
        except:
            return 0


class CommentParentAnswerSerializer(ModelSerializer):
    writer = UserOtherDetailsSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = [
            'writer',
            'body'
        ]
