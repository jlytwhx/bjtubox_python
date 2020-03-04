from . import views
from django.urls import path

urlpatterns = [
    path('comment', views.comment, name='lost_comment'),
    path('lost', views.lost, name='lost_lost')
]
