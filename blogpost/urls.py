from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comments/', views.add_comment, name='add_comment'),
    path('get-token', views.get_token, name='get_token')
]
