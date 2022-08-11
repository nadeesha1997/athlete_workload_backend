from django.urls import path

from predict.views import PredictView, ScheduleView, WeeklyWorkloadView, WorkloadListView, WorkloadAllView

urlpatterns = [
    path('<str:day>', PredictView.as_view()),
    path('schedule/', ScheduleView.as_view()),
    path('week/<str:day>', WeeklyWorkloadView.as_view()),
    path('day/today/', WorkloadListView.as_view()),
    path('workload/all/', WorkloadAllView.as_view())
]
