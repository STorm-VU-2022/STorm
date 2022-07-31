from django.db import models
from users.models import Teacher
from django.utils.translation import gettext_lazy as _

import secrets
import string


def group_key_generator():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(16))
    return password


class Methodic_group(models.Model):
    # ID - Django by default creates it and assigns it as PK
    name = models.CharField(max_length=100, verbose_name='Methodic group\'s name', unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Created at')        # To be set only 1 time
    creator = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='group_creator', verbose_name='group creator')
    description = models.TextField(verbose_name='Description')      # By default blank=false => description is mandatory
    short_description = models.TextField(max_length=140, verbose_name='Short Description', blank=True)
    photo = models.ImageField(blank=True, upload_to='group_photos/%Y/%m/%d', verbose_name=_('Group Photo'))

    # = = = = = M2M relationships = = = = =
    participates_in = models.ManyToManyField(Teacher, through='Participates_in', verbose_name='members',
                                             related_name='participants')
    invitations = models.ManyToManyField(Teacher, through='Invites', verbose_name='Invitations', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Methodic group"        # Name of your model in single form
        verbose_name_plural = "Methodic groups"        # Name of your model in plural form
        ordering = ['name', 'creation_date', ]


class Participates_in(models.Model):
    member = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                               related_name='group_member',
                               verbose_name='group_member')  # No need to have records with missing teachers
    group = models.ForeignKey(Methodic_group, on_delete=models.CASCADE, related_name='group')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return "\n" + self.group.__str__() + " | User " + self.member.__str__() + " (is_accepted: " + str(self.is_accepted) + ")"

    class Meta:
        verbose_name_plural = 'Participants'


class Invites(models.Model):
    invited_user = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                     related_name='invited_user',
                                     verbose_name='Invited user')  # No need to have records with missing teachers
    group = models.ForeignKey(Methodic_group, on_delete=models.CASCADE)
    invitation_date = models.DateTimeField(auto_now_add=True, verbose_name='Invitation date')

    def __str__(self):
        return "\n" + self.invited_user.__str__() + "\tis invited to\t" + self.group.__str__()

    class Meta:
        verbose_name_plural = 'Invitations'