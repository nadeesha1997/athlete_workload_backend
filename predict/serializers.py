from rest_framework import serializers

from predict.models import Predict, Workload


class PredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predict
        fields = '__all__'


class WorkloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workload
        fields = '__all__'
