from django.urls import path

from .views import sign_in, detail

urlpatterns = [
    path('sign', sign_in),
    path('detail', detail)
]
