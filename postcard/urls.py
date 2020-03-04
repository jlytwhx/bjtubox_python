from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.get_card_category_list, name='postcard_categories'),
    path('send', views.send_postcard, name='postcard_send'),
    path('my', views.get_my_card_list, name='postcard_my_card'),
    path('delete', views.delete_card, name='postcard_delete')
]
