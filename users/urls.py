from django.contrib.auth import views as auth_views
from django.urls import include, path
from . import views

# app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
