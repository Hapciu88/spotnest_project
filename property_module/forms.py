from django import forms
from .models import Property, PropertyRating

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'rental_price', 'address', 'latitude', 'longitude', 'image']

class PropertyRatingForm(forms.ModelForm):
    class Meta:
        model = PropertyRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Leave a comment (optional)'}),
        } 