from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('read/<slug:slug>/', views.BlogDetail.as_view(), name='blog_home'),
    path('', views.BlogList.as_view(), name='all_blogs'),
    path('featured/', views.blog_featured, name='featured'),
    path('blog/comment/', views.comment_ajax, name="commentAjax"),
]