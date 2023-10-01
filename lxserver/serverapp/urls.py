from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('test', views.test_token, name='test_token'),
    path('create_profile', views.create_profile, name='create_profile'),
]
