from django.shortcuts import render
from rest_framework import generics
from .serializers import MountSerializer,DeviceSerializer,ReadingSerializer
from .models import MountPlace,Device,Reading

# Create your views here.
class MountListView(generics.ListCreateAPIView):
    serializer_class=MountSerializer
    queryset=MountPlace.objects.all()

class MountView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=MountSerializer
    queryset=MountPlace.objects.all()

class DeviceListView(generics.ListCreateAPIView):
    serializer_class=DeviceSerializer
    queryset=Device.objects.all()

class DeviceView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=DeviceSerializer
    queryset=Device.objects.all()

class ReadingListView(generics.ListCreateAPIView):
    serializer_class=ReadingSerializer
    queryset=Reading.objects.all()

class ReadingView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ReadingSerializer
    queryset=Reading.objects.all()


