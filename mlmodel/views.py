from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from services.upload import merge
from sport.models import SportUser
from . import serializers
from .models import MlModel, ModelSport, TrainData


# Create your views here.
class MLModelList(generics.ListCreateAPIView):
    serializer_class = serializers.MlModelSerializer
    queryset = MlModel.objects.all()


class MlModelDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.MlModelSerializer
    queryset = MlModel.objects.all()


class ModelSportList(generics.ListCreateAPIView):
    serializer_class = serializers.SportModelSerializer
    queryset = ModelSport.objects.all()


class ModelSportDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SportModelSerializer
    queryset = ModelSport.objects.all()


class TrainDatalList(generics.ListCreateAPIView):
    serializer_class = serializers.TrainDataSerializer
    queryset = TrainData.objects.all()


class TrainDataDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TrainDataSerializer
    queryset = TrainData.objects.all()


class UpdateData(generics.GenericAPIView):
    serializer_class = serializers.TrainDataSerializer
    queryset = TrainData.objects.all()
    permission_classes = [IsAuthenticated]

    def put(self, request):
        sport = SportUser.objects.filter(user_id=request.user.id)[0]
        train_data = TrainData.objects.filter(sport=sport.sport)[0]
        print(train_data.data_set["b"])
        new_data = request.data["data_set"]
        processed_data = merge(new_data, sport)
        print(processed_data)
        # train_data.data_set+=request.data["data_set"]
        temp_data = train_data.data_set["b"] + request.data["data_set"]
        # print(temp_data)
        return Response(temp_data, status=status.HTTP_200_OK)
