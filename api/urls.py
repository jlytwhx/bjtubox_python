from django.urls import path
from . import views

urlpatterns = [
   path('point/', views.api_point, name='api_point'),
]
