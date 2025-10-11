from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register.as_view(), name='register'),
    path('login/', views.login_view.as_view(), name='login'),
    path('logout', views.logout_view.as_view(), name='logout'),
]
