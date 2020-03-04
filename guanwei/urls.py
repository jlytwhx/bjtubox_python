from django.urls import path
from .views import goto_tuisong, introduce, verify, api_guoqing, api_kaoyan, kaoyan

urlpatterns = [
    path('sport/', introduce),
    path('introduce/', introduce),
    path('jump/', goto_tuisong),
    path('api_guoqing/', api_guoqing),
    path('api_kaoyan/', api_kaoyan),
    path('h5kaoyan/', kaoyan),

    path('MP_verify_SGglzEfQCwUCafws.txt', verify),
]
