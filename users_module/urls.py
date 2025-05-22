from django.contrib import admin
from django.urls import path, include
from . import views
from .views import profile_view, profile_edit_view


app_name = 'module_users'  # This defines the namespace
urlpatterns = [
    path('/signup', views.SignUpView.as_view(), name='signup'),  # Example route for pages module
    path('/signin', views.SingInView.as_view(), name='signin'),  # Example route for pages module
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
]