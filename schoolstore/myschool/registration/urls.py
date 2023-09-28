from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name='registration'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('order_form', views.order_form, name='order_form'),
    path('load_courses', views.load_courses, name='load_courses'),
]
