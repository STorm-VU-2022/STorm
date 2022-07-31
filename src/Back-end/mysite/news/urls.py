from django.urls import path

from .views import *

urlpatterns = [
    path('search/', search, name='browse-publications'),
    path('material/', material_info, name='material-info'),
    path('upload/', material_upload, name='material-upload'),
    path('publication/<int:publication_pk>/', view_publication, name='view-publication'),
    path('user/<int:teacher_pk>', view_user, name='view-profile'),
    #     Endpoints:
    path('like_publication/<int:publication_pk>/', like_publication, name='like-publication'),
    path('download_publication_materials/<int:publication_pk>/', download_publication_materials, name='download-publication-materials'),
]