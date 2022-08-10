from django.urls import path
from . import views


urlpatterns = [
    path('', views.SportList.as_view(), name='sportlist'),
    path('<pk>', views.SportDetails.as_view(), name='sport'),
    path('activity/', views.ActivityList.as_view(), name='activitylist'),
    path('activity/<pk>', views.ActivityDetails.as_view(), name='activity'),
    path('activity/user/',views.UserActivityList.as_view(),name='user_activity'),
    path('user/', views.SportUserView.as_view(), name='sport_user_list'),
    path('user/<pk>', views.SportUserDetails.as_view(), name='sport_user'),
]