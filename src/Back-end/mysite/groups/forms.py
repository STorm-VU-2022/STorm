from django import forms
from django.forms import ModelForm, TextInput, Select, FileInput, Textarea
from .models import Methodic_group
from django.utils.translation import gettext_lazy as _


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Methodic_group
        fields = [
            'name',
            'short_description',
            'description',
            'photo',
        ]
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Group Name'),
                'aria-label': _('Group Name'),
                'aria-describedby': 'basic-addon2',
            }),
            'photo': FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/png, image/gif, image/jpeg',
            }),
            'short_description': Textarea(attrs={
                'class': 'form-control textarea-autosize',
                'placeholder': _('Short description (max 140 characters)'),
                # 'max_length': '40',
                'rows': '1',
            }),
            'description': Textarea(attrs={
                'class': 'form-control textarea-autosize',
                'placeholder': _('Full Description'),
                # 'maxlength': '250',
                'rows': '1',
            }),
        }
