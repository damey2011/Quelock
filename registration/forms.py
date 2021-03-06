
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password',
        )