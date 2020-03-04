from django.urls import path
from .views import status, index

urlpatterns = [
    path('index/', index),
    path('status/', status)
]
