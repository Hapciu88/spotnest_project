from django.contrib import admin
from .models import Property, PropertyRequest, PropertyRating

# Register your models here.
admin.site.register(Property)
admin.site.register(PropertyRequest)
admin.site.register(PropertyRating)
