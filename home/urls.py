from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.coming_soon, name='products'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
]
