from . import views
from django.urls import path

urlpatterns = [
    path('index', views.get_index_info, name='index_index'),
    path('baseinfo', views.get_base_info, name='index_base_info')
]
