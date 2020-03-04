from . import views
from django.urls import path

urlpatterns = [
    path('pv', views.get_pv, name='datashow_pv'),
]
