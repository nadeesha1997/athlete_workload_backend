from django.urls import path

from predict.views import PredictView, ScheduleView

urlpatterns=[
    path('<str:date>',PredictView.as_view()),
    path('schedule/',ScheduleView.as_view()),
]