from django.shortcuts import render
from rest_framework import generics
from . import serializers
from .models import MlModel,ModelSport,TrainData

# Create your views here.
class MLModelList(generics.ListCreateAPIView):
    serializer_class= serializers.MlModelSerializer
    queryset=MlModel.objects.all()

class MlModelDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=serializers.MlModelSerializer
    queryset=MlModel.objects.all()


class ModelSportList(generics.ListCreateAPIView):
    serializer_class= serializers.SportModelSerializer
    queryset=ModelSport.objects.all()

class ModelSportDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=serializers.SportModelSerializer
    queryset=ModelSport.objects.all()


class TrainDatalList(generics.ListCreateAPIView):
    serializer_class= serializers.TrainDataSerializer
    queryset=TrainData.objects.all()

class TrainDataDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=serializers.TrainDataSerializer
    queryset=TrainData.objects.all()
