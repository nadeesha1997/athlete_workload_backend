from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import serializers
from .models import Activity, Sport, SportUser


# Create your views here.
# class SportView(generics.GenericAPIView):
#     serializer_class=serializers.SportsSerializer
#     queryset=Sport.objects.all()

#     def post(self,request):
#         data=request.data
#         serializer=self.serializer_class(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data,status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     def get(self,request):
#         models=Sport.objects.all()
#         serializer=self.serializer_class(instance=models,many=True)
#         return Response(data=serializer.data,status=status.HTTP_200_OK)

#     def get_object(self,pk):
#         try:
#             return Sport.objects.get(pk=pk)
#         except Sport.DoesNotExist:
#             raise Http404

#     def put(self,request,pk):
#         model=self.get_object(pk)
#         serializer=self.serializer_class(model,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data,status=status.HTTP_200_OK)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk):
#         model=self.get_object(pk)
#         model.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class SportList(generics.ListCreateAPIView):
    queryset = Sport.objects.all()
    serializer_class = serializers.SportsSerializer


class SportDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sport.objects.all()
    serializer_class = serializers.SportsSerializer


class ActivityList(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer


class ActivityDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer


class SportUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SportUser.objects.all()
    serializer_class = serializers.SportUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        models = SportUser.objects.all().filter(user_id=request.user)
        print(models)
        serializer = self.serializer_class(instance=models, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SportUserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = SportUser.objects.all()
    serializer_class = serializers.SportUserSerializer


class UserActivityList(generics.GenericAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sports = SportUser.objects.filter(user_id=request.user)[0].sport
        models = Activity.objects.filter(sport=sports)
        serializer = self.serializer_class(instance=models, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
