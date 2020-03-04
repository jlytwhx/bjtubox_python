from . import views
from django.urls import path

urlpatterns = [
    path('new/', views.new_question, name='job_question_new'),
    path('questions/', views.get_question_list),
    path('answer/', views.new_answer)
]
