from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login
from rest_framework import status
from .utils import get_tokens_for_user
from rest_framework.parsers import JSONParser, FileUploadParser
from django.http.response import JsonResponse
from .serializers import UploadSerializer, SubjectSerializer
from news.models import Subject, Publication


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        email_message = "user email is " + request.user.email
        # content = {'message': 'Hello, World!'}
        content = {'message': email_message}
        return Response(content)


class LoginView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UploadView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]

    def post(self, request):
        upload_data = JSONParser().parse(request)
        upload_serializer = UploadSerializer(data=upload_data)
        if upload_serializer.is_valid():
            upload_serializer.save(creator_id=request.user)
            return JsonResponse(upload_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(upload_serializer, status=status.HTTP_400_BAD_REQUEST)


class SubjectView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return JsonResponse(serializer.data, safe=False)


class UploadMediaView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [FileUploadParser]

    def put(self, request, publication_pk, filename):
        file_obj = request.data['file']
        publication = Publication.objects.get(pk=publication_pk)
        publication.media = file_obj
        publication.save()
        return Response({'msg': 'File Uploaded Sucessfully'}, status=status.HTTP_200_OK)
