from django.urls import path
from . import views

urlpatterns = [
   path('point', views.get_stu_point, name='point_point'),
]
