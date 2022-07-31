from django import forms
from django.forms import TextInput, Select, FileInput, Textarea
from django.utils.translation import gettext_lazy as _

from groups.models import Methodic_group
from .models import Publication, Comments, Subject

GRADE_CHOICES = [(grade, grade) for grade in range(1, 13)]
LANGUAGE_CHOICES = [('Lithuanian', 'Lithuanian'), ('English', 'English'), ('Russian', 'Russian')]


class UploadFileForm(forms.ModelForm):
    subject = forms.ModelChoiceField(required=True, blank=False, label=None, empty_label=None,
                                     queryset=Subject.objects.order_by('name').all(),
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'selectpicker',
                                             'title': _('Subject'),
                                             'placeholder': 'Subject',
                                             'data-live-search': 'true',
                                             'data-live-search-placeholder': _('Search for a subject'),
                                         }))
    related_to_group = forms.ModelChoiceField(label=None, empty_label=None, blank=True, required=False,
                                              queryset=Methodic_group.objects.order_by('name').all(),
                                              widget=forms.Select(
                                                  attrs={
                                                      'class': 'selectpicker',
                                                      'title': _('Group'),
                                                      'placeholder': 'Group',
                                                      'data-live-search': 'true',
                                                      'data-live-search-placeholder': _('Search for a group'),
                                                  }))

    class Meta:
        model = Publication
        fields = [
            'title',
            'language',
            'student_year',
            'is_public',
            'short_description',
            'description',
            'photo',
            'media',
            'subject',
            'related_to_group',
        ]
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Material Title'),
                'aria-label': _('Material Title'),
                'aria-describedby': 'basic-addon2',
            }),
            'student_year': Select(attrs={
                'class': 'selectpicker',
                'title': _('Grade'),
                'placeholder': 'Grade',
                'data-live-search': 'true',
                'data-live-search-placeholder': _('Search ...'),

            }, choices=GRADE_CHOICES),
            'language': Select(attrs={
                'class': 'selectpicker',
                'title': _('Language'),
                'placeholder': _('Language'),
                'data-live-search': 'true',
                'data-live-search-placeholder': _('Search ...'),
            }, choices=LANGUAGE_CHOICES),
            'media': FileInput(attrs={
                'type': 'file',
                'class': 'form-control',
            }),
            'photo': FileInput(attrs={
                # 'type': 'file',
                # 'name': 'file-3',
                # 'id': 'file-3',
                'class': 'form-control',
                'accept': 'image/png, image/gif, image/jpeg',
            }),
            'short_description': Textarea(attrs={
                'class': 'form-control textarea-autosize',
                'placeholder': _('Short description (max 140 characters)'),
                'rows': '1',
            }),
            'description': Textarea(attrs={
                'class': 'form-control textarea-autosize',
                'placeholder': _('Full Description'),
                'rows': '1',
            }),
        }


class CommentPublicationForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment', ]
        widgets = {
            'comment': Textarea(attrs={
                'class': 'form-control textarea-autosize',
                'placeholder': 'Your commentary',
                'rows': '3',
            }),
        }
