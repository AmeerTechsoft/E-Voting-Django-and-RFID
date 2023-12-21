from django.urls import path
from . import views


urlpatterns = [
    path('', views.account_login, name="account_login"),
    path('register/', views.account_register, name="account_register"),
    path('get_rfid_data/', views.get_rfid_data, name='get_rfid_data'),
    path('get_latest_rfid_data/', views.get_latest_rfid_data, name='get_latest_rfid_data'),
    path('logout/', views.account_logout, name="account_logout"),
]
