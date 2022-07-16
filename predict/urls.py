from django.urls import path

from predict.views import PredictView

urlpatterns=[
    path('<str:date>',PredictView.as_view())
]