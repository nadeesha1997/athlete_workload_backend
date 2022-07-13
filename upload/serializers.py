from rest_framework import serializers
from .models import Upload, MergeData


class UploadSerializer(serializers.ModelSerializer):
    # user=serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Upload
        exclude = ['user', 'date']
        # fields = ['date','data']

    # def validate(self, attrs):
    #     return super().validate(attrs)
    #
    # def create(self, validated_data):
    #     validated_data['user'] = self.context.get('user').id
    #     return super().create(validated_data)


class MergeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MergeData
        # exclude = ['user', 'date']
        fields='__all__'
