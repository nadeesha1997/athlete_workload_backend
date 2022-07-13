from django.urls import path
from . import views


urlpatterns = [
    path('', views.UploadListView.as_view(), name='uploadlist'),
    path('<pk>', views.UploadView.as_view(), name='upload'),
    path('user/',views.ViewUser.as_view()),
    path('upload/',views.UploadWithUserView.as_view()),
    path('merge/<str:date>',views.MergeDataView.as_view())
]