from django.urls import path
from .views import get_recent_message

urlpatterns = [
    path('recent/', get_recent_message, name='room_recent'),
]
