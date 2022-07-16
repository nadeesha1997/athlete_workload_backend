from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from predict.models import Predict
from rest_framework.response import Response
from rest_framework import status
from mlmodel.models import MlModel, ModelSport

from predict.serializers import PredictSerializer, WorkloadSerializer
from services.prediction import predict
from datetime import datetime

# Create your views here.
from sport.models import SportUser, Activity
from upload.models import MergeData


class PredictView(generics.GenericAPIView):
    serializer_class = PredictSerializer
    queryset = Predict.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request,date):
        all_data=MergeData.objects.all().filter(user_id=request.user.id,date=date)[0]
        test_data = all_data.data["har"]
        sport=SportUser.objects.filter(user_id=request.user.id)[0].sport
        ml_model=ModelSport.objects.filter(sport=sport)[0].first_model
        # try:
        output = predict(ml_model.model_file.path, test_data)
        activities=Activity.objects.filter(sport=sport)
        activity_count={}
        for activity in activities:
            activity_count[activity.id_field]=0
        for val in output:
            activity_count[val]=activity_count[val]+1
        heart_rate=all_data.data["hr"]
        average_heart_rate=0
        if len(heart_rate)>0:
            average_heart_rate = sum(heart_rate) / len(heart_rate)
        user=all_data.user
        model_date=all_data.date
        final_data={
            "workload_data":{"har":activity_count,"hr":average_heart_rate},
            "date":model_date,
            "user":user.id
        }
        workload_serializer=WorkloadSerializer(data=final_data)
        if workload_serializer.is_valid(raise_exception=True):
            workload_serializer.save()
            return Response(workload_serializer.data,status=status.HTTP_200_OK)
        return Response(workload_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({'msg':'prediction failed'}, status=status.HTTP_400_BAD_REQUEST)