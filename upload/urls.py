from django.urls import path
from . import views


urlpatterns = [
    path('', views.UploadListView.as_view(), name='uploadlist'),
    path('<pk>', views.UploadView.as_view(), name='upload'),
]