"""bjtubox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def corp_check(request):
    return HttpResponse('ytmTcadgwQ1GNbDk')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('network/', include('network.urls')),
    path('ecard/', include('ecard.urls')),
    path('sport/', include('sport.urls')),
    path('course/', include('course.urls')),
    path('lost/', include('lost.urls')),
    path('schedule/', include('schedule.urls')),
    path('index/', include('index.urls')),
    path('freeclass/', include('freeclass.urls')),
    path('point/', include('point.urls')),
    path('person/', include('person.urls')),
    path('upload/', include('upload.urls')),
    path('datashow/', include('datashow.urls')),
    path('exam/', include('exam.urls')),
    path('postcard/', include('postcard.urls')),
    path('cet/', include('cet.urls')),
    path('room/', include('chatroom.urls')),
    path('morning/', include('morning.urls')),
    path('job/question/', include('job_question.urls')),
    path('bigdata/', include('bigdata.urls')),
    path('guanwei/', include('guanwei.urls')),
    path('api/', include('api.urls')),
    path('job/', include('job.urls')),
    path('cc/', include('course_center.urls')),
    path('WW_verify_ytmTcadgwQ1GNbDk.txt', corp_check)
]
