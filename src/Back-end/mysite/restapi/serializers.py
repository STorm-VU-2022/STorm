from rest_framework import serializers
from news.models import Publication, Subject


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ('id',
                  'title',
                  'language',
                  'student_year',
                  'is_public',
                  'short_description',
                  'description',
                  'subject',
                  'media',
                  )
        extra_kwargs = {'creator_id': {'read_only': True}}


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']