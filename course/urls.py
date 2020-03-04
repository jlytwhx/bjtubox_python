from . import views
from django.urls import path

urlpatterns = [
    path('detail', views.get_detail_info, name='course_detail'),
    path('search', views.search, name='course_search'),
    path('base', views.get_base_info, name='course_base')
]
