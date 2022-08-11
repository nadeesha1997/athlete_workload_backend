from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from predict.models import Predict, Workload
from rest_framework.response import Response
from rest_framework import status
from mlmodel.models import MlModel, ModelSport

from predict.serializers import PredictSerializer, WorkloadSerializer
from services.prediction import predict
from datetime import datetime

# Create your views here.
from services.workload import next_day_workload, activity_acwr, workload_of_week
from sport.models import SportUser, Activity
from upload.models import MergeData


class PredictView(generics.GenericAPIView):
    serializer_class = PredictSerializer
    queryset = Predict.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, day):
        all_data = MergeData.objects.all().filter(user_id=request.user.id, date=day)[0]
        test_data = all_data.data["har"]
        sport = SportUser.objects.filter(user_id=request.user.id)[0].sport
        ml_model = ModelSport.objects.filter(sport=sport)[0].first_model
        # try:
        output = predict(ml_model.model_file.path, test_data)
        activities = Activity.objects.filter(sport=sport)
        activity_count = {}
        for activity in activities:
            activity_count[activity.id_field] = 0
        for val in output:
            activity_count[val] = activity_count[val] + 1
        heart_rate = all_data.data["hr"]
        average_heart_rate = 0
        if len(heart_rate) > 0:
            average_heart_rate = sum(heart_rate) / len(heart_rate)
        user = all_data.user
        model_date = all_data.date
        wl_data = {"har": activity_count, "hr": average_heart_rate}
        final_data = {
            "workload_data": wl_data,
            "date": model_date,
            "user": user.id
        }
        workload_serializer = WorkloadSerializer(data=final_data)
        if workload_serializer.is_valid(raise_exception=True):
            workload_serializer.save()
            return Response(workload_serializer.data, status=status.HTTP_200_OK)
        return Response(workload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request,date):
    #     user=request.user
    #     workload_data = Workload.objects.filter(user_id=request.user.id)
    #     acwr_val=activity_acwr(list(workload_data))
    #     daily_workload=workload_data.filter(date=date)
    #     list_daily_workload=list(daily_workload)
    #     ret_data=[]
    #     ret_data.append(daily_workload)
    #     acwr_vals=[]
    #     for key in acwr_val:
    #         acwr_vals.append(acwr_val[key])
    #     return Response(data=list_daily_workload,status=status.HTTP_200_OK)
    def get(self, request, day):
        user = request.user
        workload_data = Workload.objects.filter(user_id=request.user.id)
        acwr_val = activity_acwr(list(workload_data), datetime.today().date())

        # daily_workload=workload_data.filter(date=date)
        # list_daily_workload=list(daily_workload)
        # ret_data=[]
        # ret_data.append(acwr_val)
        # ret_data.append(list_daily_workload)
        # ret_data.append(daily_workload)
        # acwr_vals=[]
        # for key in acwr_val:
        #     acwr_vals.append(acwr_val[key])
        return Response(data=acwr_val, status=status.HTTP_200_OK)


class WorkloadListView(generics.GenericAPIView):
    serializer_class = WorkloadSerializer
    queryset = Workload.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        models = Workload.objects.filter(user=request.user).filter(date=datetime.today().date())
        print(datetime.today().date())
        serializer = self.serializer_class(instance=models, many=True)
        # if serializer.is_valid(raise_exception=True):
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkloadAllView(generics.GenericAPIView):
    serializer_class = WorkloadSerializer
    queryset = Workload.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        models = Workload.objects.filter(user=request.user)
        serializer = self.serializer_class(instance=models, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ScheduleView(generics.GenericAPIView):
    serializer_class = PredictSerializer
    queryset = Predict.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        workload_data = Workload.objects.filter(user_id=request.user.id)
        sport = SportUser.objects.filter(user_id=request.user.id)[0].sport
        activities = Activity.objects.filter(sport=sport)
        next_day_min = next_day_workload(workload_data, 0.8, activities)
        next_day_max = next_day_workload(workload_data, 1.3, activities)
        schedule = [next_day_min, next_day_max]
        return Response(schedule, status=status.HTTP_200_OK)


class WeeklyWorkloadView(generics.GenericAPIView):
    serializer_class = PredictSerializer
    queryset = Predict.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, day):
        weekly_acwr = []
        user = request.user
        workload_data = Workload.objects.filter(user_id=request.user.id)
        lst = list(workload_data)
        lst.reverse()
        acwr_val = workload_of_week(lst, datetime.today().date())
        return Response(acwr_val, status=status.HTTP_200_OK)
# class HrWorkloadView(generics.GenericAPIView):
#     serializer_class = PredictSerializer
#     queryset = Predict.objects.all()
#     permission_classes = [IsAuthenticated]
#     def get(self,request,day):
