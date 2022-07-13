from dataclasses import fields
from pyexpat import model

# from sport.serializers import SportsSerializer
from .models import MlModel, ModelSport,TrainData
from rest_framework import serializers

class MlModelSerializer(serializers.ModelSerializer):
    model_name=serializers.CharField(max_length=50)
    model_file=serializers.FileField()

    class Meta:
        model=MlModel
        fields='__all__'


class TrainDataSerializer(serializers.ModelSerializer):
    data_set=serializers.JSONField()
    # sport=SportsSerializer(many=False)

    class Meta:
        model=TrainData
        fields='__all__'


class SportModelSerializer(serializers.ModelSerializer):
    # model=MlModelSerializer(many=True)
    # sport=SportsSerializer(many=True)
    class Meta:
        model=ModelSport
        fields='__all__'
