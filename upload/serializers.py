from rest_framework import serializers
from .models import Upload


class UploadSerializer(serializers.ModelSerializer):
    # user=serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Upload
        exclude=['user']
        # fields = ['date','data']

    # def validate(self, attrs):
    #     return super().validate(attrs)
    #
    # def create(self, validated_data):
    #     validated_data['user'] = self.context.get('user').id
    #     return super().create(validated_data)
