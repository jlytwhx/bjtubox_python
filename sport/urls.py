from . import views
from django.urls import path

urlpatterns = [
    path('upload', views.upload_data, name='sport_upload'),
]
