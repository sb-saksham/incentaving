from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import LoginView, RegisterView, subscribe, AccountsHome, AccountsEmailActivation

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', AccountsHome.as_view(), name="home"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('news/subscribe/', subscribe, name='subscribe'),
    re_path(r'^activate/(?P<key>[0-9A-Za-z]+)/$', AccountsEmailActivation.as_view(), name='email-activation'),
    path('reactivate/', AccountsEmailActivation.as_view(), name='resend-activation'),
]
