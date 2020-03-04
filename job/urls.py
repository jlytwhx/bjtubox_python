from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_to_bjtu_job, name='job_login'),
]
