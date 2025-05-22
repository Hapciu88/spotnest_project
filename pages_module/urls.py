from django.contrib import admin
from django.urls import path
from . import views

app_name = 'module_pages'  # This defines the namespace
urlpatterns = [
    path('', views.LandingView.as_view(), name='home'),  # Example route for pages module
]
