from django.urls import path
from .views import *

urlpatterns = [
    path('', group_search),
    path('group-creation/', group_creation, name='create-group'),
    path('group-profile/<int:group_pk>', group_profile, name='profile-group'),
    path('search-group/', group_search, name='group-search'),
    path('group-edit/', group_edit, name='edit-group'),
    path('my-groups/', my_groups, name='my-groups'),
    #     Endpoints:
    path('group-invite-user/<int:user_pk>', group_invite_user, name='group-invite-user'),
    path('group/<int:group_pk>/follow', group_follow, name='group-follow'),
    path('group/<int:group_pk>/unfollow', group_unfollow, name='group-unfollow'),
    path('group/<int:group_pk>/unfollow/<str:do_redirect_to_group>', group_unfollow, name='group-unfollow'),
    path('group-invitation/<int:invitation_pk>/accept', group_invitation_accept, name='group-invitation-accept'),
    path('group-invitation/<int:invitation_pk>/reject', group_invitation_reject, name='group-invitation-reject')
]

