from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UploadSerializer
from .models import Upload
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UploadListView(generics.ListCreateAPIView):
    serializer_class=UploadSerializer
    queryset=Upload.objects.all()
    permission_classes = [IsAuthenticated]

class UploadView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UploadSerializer
    queryset=Upload.objects.all()
    permission_classes = [IsAuthenticated]

class UploadWithUserView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=UploadSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ViewUser(generics.GenericAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        if user is not None:
            print(user.id)
            return Response(data={"val":"done"},status=status.HTTP_200_OK)
        return Response(data={"err":"please login"},status=status.HTTP_401_UNAUTHORIZED)