from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, Select, FileInput, Textarea
from django.contrib.auth import get_user_model
from .models import Recommends
from django.utils.translation import gettext_lazy as _

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, label=_("Full name"))
    email = forms.EmailField(max_length=254, label=_("Email"))
    password1 = forms.CharField(label=_('Enter password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('full_name', 'email', 'password1', 'password2', )
        # help_texts = {
        #     "username": None,
        # }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'self_description',
            'profile_picture',
            'profession',
            'facebook_link',
            'twitter_link',
            'instagram_link',
            'linkedin_link',
        ]

        widgets = {
            'profession': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Profession'),
                'aria-label': _('Profession'),
                'aria-describedby': 'basic-addon2',
            }),
            'profile_picture': FileInput(attrs={
                'type': 'file',
                'class': 'form-control',
            }),
            'self_description': Textarea(attrs={
                'class': 'form-control textarea-autosize',
                'placeholder': _('Full description about you'),
                'rows': '1',
            }),
            'facebook_link': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Facebook link (optional)'),
                'aria-label': 'Facebook'
            }),
            'twitter_link': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Twitter link (optional)'),
                'aria-label': 'Twitter'
            }),
            'instagram_link': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Instagram link (optional)'),
                'aria-label': 'Instagram'
            }),
            'linkedin_link': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('LinkedIn link (optional)'),
                'aria-label': 'LinkedIn'
            }),
        }


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommends
        fields = ('recommendation_text', )
        widgets = {
            'recommendation_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }