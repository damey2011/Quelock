from django import forms
from django.forms import ModelForm
from account.models import UserOtherDetails


class AccountUpdateForm(ModelForm):
    class Meta:
        model = UserOtherDetails
        fields = [
            'bio',
            'college',
            'works',
            'lives',
            'facebook_link',
            'twitter_link',
            'linked_in_profile',
            'display_picture'
        ]
        widgets = {'bio': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Will appear after you name on your answers'
            }
        ),
            'college': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Where did you school'
                }
            ),
            'works': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Where do you work'
                }),
            'lives': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Where do you live in'
                }),
            'facebook_link': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Facebook Profile URL'
                }),
            'twitter_link': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Twitter Profile URL'
                }),
            'linked_in_profile': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your LinkedIn Profile URL'
                })
        }
