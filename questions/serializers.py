from rest_framework.serializers import ModelSerializer
from account.serializers import UserSerializer

from questions.models import Question


class QuestionSerializer(ModelSerializer):
    author = UserSerializer

    class Meta:
        model = Question
        fields = '__all__'
