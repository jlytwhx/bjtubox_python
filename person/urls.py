from . import views
from django.urls import path

urlpatterns = [
    path('search', views.search, name='person_search'),
]
