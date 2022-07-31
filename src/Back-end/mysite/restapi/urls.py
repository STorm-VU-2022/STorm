from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('login/', views.LoginView.as_view(), name='api-login'),
    path('upload/', views.UploadView.as_view(), name='api-upload'),
    path('subjects/', views.SubjectView.as_view(), name='api-subjects'),
    path('publication/<int:publication_pk>/<str:filename>/', views.UploadMediaView.as_view(), name='api-media-upload'),
]
