from rest_framework import serializers
from .models import Sport, Activity, SportUser


class SportsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    # activities=ActivitySerializer(many=True)

    class Meta:
        model = Sport
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    id_field = serializers.IntegerField()
    name = serializers.CharField(max_length=50)

    # sport=SportsSerializer(many=True)

    class Meta:
        model = Activity
        fields = '__all__'


class SportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportUser
        fields = ['sport']
