from . import views
from django.urls import path

urlpatterns = [
    path('image', views.upload_image, name='upload_image'),
]
