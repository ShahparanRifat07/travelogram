from django.urls import path
from .views import create_post,detail_post

app_name = 'post'
urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('detail/<int:pk>', detail_post, name='detail_post'),
]