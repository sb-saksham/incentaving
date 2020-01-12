from django.urls import path
from . import views

app_name = 'action'

urlpatterns = [
    path('', views.user_home, name='home'),
    path('calculate/', views.take_cc, name='cc_take'),
]
