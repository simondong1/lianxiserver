from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_image, name='upload_image'),
    path('get/<str:usr_name>', views.get_image, name='get_image'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('test', views.test_token, name='test_token'),
]
