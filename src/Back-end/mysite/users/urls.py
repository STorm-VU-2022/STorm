from django.urls import path, include

from .views import *
from news.views import view_user

urlpatterns = [
    path('', index),
    path('profile/', profile, name="profile"),
    path('register/', register, name="register"),
    path('edit/', edit, name="edit"),
    path('leaderboard/', leaderboard, name="leaderboard"),
    path('', include('django.contrib.auth.urls')),
    path('logout/', logout_view),
    path('user/<int:teacher_pk>', view_user, name='view-profile'),
    path('search-user/', user_search, name='user-search'),
    #     REST API endpoints:
    path('add-profile-recommendation/<int:profile_pk>', add_profile_recommendation, name='add-profile-recommendation')
]
