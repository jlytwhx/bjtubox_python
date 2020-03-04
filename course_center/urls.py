from django.urls import path, re_path
from .views import jump, cc_session, down_file

urlpatterns = [
    re_path(r'jump/file/', down_file),
    re_path(r'jump/', jump),
    path('session/', cc_session)
]
