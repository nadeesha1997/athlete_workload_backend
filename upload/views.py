from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UploadSerializer, MergeDataSerializer
from .models import Upload, MergeData
from rest_framework.permissions import IsAuthenticated
from datetime import date


# Create your views here.
class UploadListView(generics.ListCreateAPIView):
    serializer_class = UploadSerializer
    queryset = Upload.objects.all()
    # permission_classes = [IsAuthenticated]


class UploadView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UploadSerializer
    queryset = Upload.objects.all()
    permission_classes = [IsAuthenticated]


class UploadWithUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UploadSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, date=date.today())
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewUser(generics.GenericAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user is not None:
            print(user.id)
            return Response(data={"val": "done"}, status=status.HTTP_200_OK)
        return Response(data={"err": "please login"}, status=status.HTTP_401_UNAUTHORIZED)


class MergeDataView(generics.GenericAPIView):
    queryset = MergeData.objects.all()
    serializer_class = MergeDataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, date=None):
        datalist = Upload.objects.filter(date=date, user_id=request.user.id)
        # date = datalist[0].date
        data = []
        for item in datalist:
            data=data+item.data
            # item.delete()
        print(data)
        savedata = {
            'user': request.user.id,
            'date': date,
            'data': data
        }
        serializer = self.serializer_class(data=savedata)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
