from django.urls import path
from . import views


urlpatterns = [
    path('mount/', views.MountListView.as_view(), name='mountlist'),
    path('mount/<pk>', views.MountView.as_view(), name='mount'),
    path('', views.DeviceListView.as_view(), name='devicelist'),
    path('<pk>', views.DeviceView.as_view(), name='device'),
    path('reading/', views.ReadingListView.as_view(), name='readinglist'),
    path('reading/<pk>', views.ReadingView.as_view(), name='reading'),
]