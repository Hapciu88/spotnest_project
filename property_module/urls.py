from django.contrib import admin
from django.urls import path

from pages_module.urls import app_name
from .views import property_map_view, property_list_json, add_property_view, property_detail_view, my_properties_view, edit_property_view, landlord_requests_view

app_name = 'module_property'  # This defines the namespace
urlpatterns = [
       path('admin/', admin.site.urls),
       path('map/', property_map_view, name='property_map'),
       path('list-json/', property_list_json, name='property_list_json'),
       path('add/', add_property_view, name='add_property'),
       path('my-properties/', my_properties_view, name='my_properties'),
       path('<int:pk>/edit/', edit_property_view, name='edit_property'),
       path('requests/', landlord_requests_view, name='landlord_requests'),
       path('<int:pk>/', property_detail_view, name='property_detail'),
]
