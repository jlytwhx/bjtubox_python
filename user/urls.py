from . import views
from django.urls import path

urlpatterns = [
    path('login', views.login, name='user_login'),
    path('verifyCode', views.get_verify_code, name='user_verify_code'),
    path('verify', views.verify, name='user_verify'),
    path('uploadWxInfo', views.upload_user_info, name='user_upload_wx_info'),
    path('logout', views.logout, name='user_logout'),
]
