from dataclasses import fields
from rest_framework import serializers
from .models import Sport,Activity



class ActivitySerializer(serializers.ModelSerializer):
    id_field=serializers.IntegerField()
    name=serializers.CharField(max_length=50)
    # sport=SportsSerializer(many=True)

    class Meta:
        model=Activity
        fields='__all__'

class SportsSerializer(serializers.ModelSerializer):
    name=serializers.CharField()
    activities=ActivitySerializer(many=True)

    class Meta:
        model=Sport
        fields='__all__'