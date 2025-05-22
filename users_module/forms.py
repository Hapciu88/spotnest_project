from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'age', 'about', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about'].label = "Tell us about yourself or your property"

class TenantProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'hashtags', 'age', 'orientation', 'income', 'about']
        widgets = {
            'hashtags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. #quiet,#nonsmoker'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
