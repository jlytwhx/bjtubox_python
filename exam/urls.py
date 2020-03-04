from django.urls import path
from .views import get_exam_info

urlpatterns = [
    path('show/', get_exam_info, name='exam_info')
]
