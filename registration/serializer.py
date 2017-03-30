from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        # fields = ('username', 'first_name', 'last_name', 'email')  # To send selected fields in the model as JSON response

        # But to send all, you just need to put
        fields = '__all__'
