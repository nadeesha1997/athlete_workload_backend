from django.shortcuts import render
from rest_framework import generics
from predict.models import Predict
from rest_framework.response import Response
from rest_framework import status
from mlmodel.models import MlModel

from predict.serializers import PredictSerializer
from services.prediction import predict

# Create your views here.
class PredictView(generics.GenericAPIView):
    serializer_class=PredictSerializer
    queryset=Predict.objects.all()
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            ml_model_id=Predict.objects.get(date=data.date)[0].ml_model
            ml_model=MlModel.objects.get(id=ml_model_id)
            output=predict(ml_model,data)
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)