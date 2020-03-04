from . import views
from django.urls import path

urlpatterns = [
    path('info', views.get_info, name='network_info'),
    path('offline',views.offline,name='network_offline')
]
