from django import forms
from django.forms import ModelForm
from topics.models import Topic


class TopicCreateUpdateForm(ModelForm):
    class Meta:
        model = Topic
        fields = [
            'title',
            'desc',
            'image_name'
        ]
        widgets = {'title': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Topic Title'
            }
        ),
            'desc': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write a brief intro or description about the topic',
                    'rows': '3'
                }
            )
        }