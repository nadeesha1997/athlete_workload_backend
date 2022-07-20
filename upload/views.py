from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from device.models import Device, MountPlace, SportMountPlace, Reading
from sport.models import Sport, SportUser
from .serializers import UploadSerializer, MergeDataSerializer
from .models import Upload, MergeData
from rest_framework.permissions import IsAuthenticated
from datetime import date
import numpy as np


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

    def post(self, request, date=None):
        datalist = Upload.objects.filter(date=date, user_id=request.user.id)
        sport_id = SportUser.objects.filter(user_id=request.user.id)[0].sport_id
        places = SportMountPlace.objects.filter(sport_id=sport_id)
        devices = Device.objects.all()
        device_selected = []
        for device in devices:
            for place in places:
                if device.mount_id == place.id:
                    device_selected.append(device)
        read = {}
        for d in device_selected:
            read[d.id] = []
        for dataval in datalist:
            temp_data = dataval.data
            for temp_data_val in temp_data:
                read[temp_data_val['1']].append(temp_data_val)
        maximum_time = []
        minimum_length = []
        for key in read:
            temp = []
            temp.append(read[key])
            temp.sort(key=lambda x: x[0]['3'])
            read[key] = temp
            print(read[key][0][0]['3'])
            maximum_time.append(read[key][0][0]['3'])
        maximum = max(maximum_time)
        print('max' + str(maximum))
        for key in read:
            for val in read[key][0]:
                if val['3'] < maximum:
                    read[key][0].remove(val)
        for key in read:
            minimum_length.append(len(read[key][0]))
        # min_len = min(len(read[1][0]), len(read[2][0]), len(read[3][0]))
        min_len = min(minimum_length)
        for key in read:
            length = len(read[key][0]) - min_len
            if length > 0:
                for i in range(length):
                    read[key][0].pop(-1)
        har_data = {}
        heart_rate = []
        sport_place_list = list(places)
        place_list = []
        for place in sport_place_list:
            place_list.append(place.place)
        place_list.sort(key=lambda x: x.mounting_order)
        # print(len(read[device_selected[0].id][0]))
        for j in range(len(read[device_selected[0].id][0])):
            har_data[j]=[]
        for j in range(len(read[device_selected[0].id][0])):
            for mount_place in places:
                for d in device_selected:
                    if d.mount == mount_place.place:
                        # print(read[d.id][0][j]['4'])
                        har_data[j].append(read[d.id][0][j]['4'])
                        har_data[j].append(read[d.id][0][j]['5'])
                        har_data[j].append(read[d.id][0][j]['6'])
                        har_data[j].append(read[d.id][0][j]['7'])
                        har_data[j].append(read[d.id][0][j]['8'])
                        har_data[j].append(read[d.id][0][j]['9'])
                        if d.mount.mounting_order==1:
                            if read[d.id][0][j]['10']>60:
                                heart_rate.append(read[d.id][0][j]['10'])
        final_data={
            "har":har_data,
            "hr":heart_rate
        }
        # final_data= [har_data, heart_rate]
        export_data = {
            "data": final_data,
            "user": request.user.id,
            "date": date,
            # "times":len(har_data)
        }
        # print(read[1])
        serializer = self.serializer_class(data=export_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            for data in datalist:
                data.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'data': 'merge failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, date=None):
        models = MergeData.objects.filter(user_id=request.user.id,date=date)
        serializer = self.serializer_class(instance=models, many=True)
        userdata=list(serializer.data)
        # print(len(userdata[0]['data']['har']))
        # print(serializer.data)
        return_data={"data":serializer.data,"len":len(userdata[0]['data']['har'])}
        return Response(return_data, status=status.HTTP_200_OK)

class MergeView(generics.ListCreateAPIView):
    serializer_class = MergeDataSerializer
    queryset = MergeData.objects.all()

class MergeViewD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MergeDataSerializer
    queryset = MergeData.objects.all()
