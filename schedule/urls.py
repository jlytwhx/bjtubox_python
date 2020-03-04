from . import views
from django.urls import path

urlpatterns = [
    path('schedule', views.get_schedule, name='schedule_schedule'),
    path('classmate', views.get_classmate, name='schedule_classmate'),
    path('recommendation', views.get_intelligent_recommendation, name='schedule_recommendation')
]
