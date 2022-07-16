from rest_framework import serializers
from .models import MountPlace, Device, Reading, SportMountPlace


class MountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MountPlace
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = '__all__'


class SportMountPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportMountPlace
        fields = '__all__'
