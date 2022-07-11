from django.shortcuts import render
from rest_framework import generics
from .serializers import UploadSerializer
from .models import Upload

# Create your views here.
class UploadListView(generics.ListCreateAPIView):
    serializer_class=UploadSerializer
    queryset=Upload.objects.all()

class UploadView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UploadSerializer
    queryset=Upload.objects.all()


