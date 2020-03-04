from . import views
from django.urls import path

urlpatterns = [
    path('freeclass', views.get_free_classroom, name='freeclass_get'),
    path('classroom', views.get_classroom_status, name='freeclass_status')
]
