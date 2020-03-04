from django.urls import path
from .views import get_verify_code, get_cet_number

urlpatterns = [
    path('code/', get_verify_code, name='cet_code'),
    path('number/', get_cet_number, name='cet_number')
]
