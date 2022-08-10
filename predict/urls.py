from django.urls import path

from predict.views import PredictView, ScheduleView, WeeklyWorkloadView

urlpatterns = [
    path('<str:day>', PredictView.as_view()),
    path('schedule/', ScheduleView.as_view()),
    path('week/<str:day>',WeeklyWorkloadView.as_view())
]
