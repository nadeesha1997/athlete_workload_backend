from django.urls import path
from . import views


urlpatterns = [
    path('', views.MLModelList.as_view(), name='modellist'),
    path('<pk>', views.MlModelDetails.as_view(), name='model'),
    path('sport/', views.ModelSportList.as_view(), name='modelsportlist'),
    path('sport/<pk>', views.ModelSportDetails.as_view(), name='modelsport'),
    path('data/', views.TrainDatalList.as_view(), name='datalist'),
    path('data/<pk>', views.TrainDataDetails.as_view(), name='data'),
]