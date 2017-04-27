from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from account.models import UserOtherDetails, UserFollowings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
        ]


class UserOtherDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserOtherDetails
        fields = '__all__'


class FollowingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    reverse_follows = SerializerMethodField()

    class Meta:
        model = UserFollowings
        fields = [
            'user',
            'is_following',
            'reverse_follows'
        ]

    def get_user(self, obj):
        return UserOtherDetailsSerializer(obj.user.profile).data

    def get_is_following(self, obj):
        return UserOtherDetailsSerializer(obj.is_following.profile).data

    def get_reverse_follows(self, obj):
        return obj.follows(self.context.get('request').user, 1)


class FollowersSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    reverse_follows = SerializerMethodField()

    class Meta:
        model = UserFollowings
        fields = [
            'user',
            'is_following',
            'reverse_follows'
        ]

    def get_user(self, obj):
        return UserOtherDetailsSerializer(obj.user.profile).data

    def get_is_following(self, obj):
        return UserOtherDetailsSerializer(obj.is_following.profile).data

    def get_reverse_follows(self, obj):
        return obj.follows(self.context.get('request').user, 2)
