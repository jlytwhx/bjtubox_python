from . import views
from django.urls import path

urlpatterns = [
    path('balance', views.get_user_ecard_balance, name='ecard_balance'),
    path('records', views.get_user_ecard_records, name='ecard_records'),
    path('month_data', views.get_month_records, name='ecard_month'),
    path('category', views.get_category_list, name='category')
]
