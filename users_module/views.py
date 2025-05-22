from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserSignupForm, TenantProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()  # Using built-in Django form
        return render(request, 'module_users/signup.html', {'form': form})

    def post(self, request):
        # Get the data manually
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        user_type = request.POST.get('user_type', 'tenant')  # Default to 'tenant'
        age = request.POST.get('age', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = {}

        # Validate required fields
        if not username:
            errors['username'] = "Username is required."
        if not email:
            errors['email'] = "Email is required."
        if not first_name:
            errors['first_name'] = "First name is required."
        if not last_name:
            errors['last_name'] = "Last name is required."
        if not password1 or not password2:
            errors['password'] = "Both password fields are required."
        if password1 and password1 != password2:
            errors['password'] = "Passwords do not match."

        # Validate username uniqueness
        if CustomUser.objects.filter(username=username).exists():
            errors['username'] = "This username is already taken."

        # Validate email uniqueness
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = "An account with this email already exists."

        # Validate age (optional)
        if age:
            try:
                age = int(age)
                if age < 18:
                    errors['age'] = "You must be at least 18 years old."
            except ValueError:
                errors['age'] = "Age must be a number."

        # If there are errors, re-render the form with errors
        if errors:
            return render(request, 'module_users/signup.html', {'errors': errors, 'form_data': request.POST})

        # Create and save the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            age=age if age else None,
            about='',
            password=password1
        )

        # Auto-login the user
        login(request, user)
        return redirect('module_pages:home')  # Redirect to homepage


class SingInView(View):
    def get(self, request):
        form = CustomUserSignupForm()  # Using Django's built-in form
        return render(request, 'module_users/signin.html', {'form': form})



    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember_me = request.POST.get('remember_me')

        errors = {}

        # Validate required fields
        if not username:
            errors['username'] = "Username is required."
        if not password:
            errors['password'] = "Password is required."

        if errors:
            return render(request, 'module_users/signin.html', {'errors': errors, 'form_data': request.POST})

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # If 'Remember Me' is not checked, make session expire when browser closes
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes

            return redirect('module_pages:home')  # Redirect to homepage after login
        else:
            errors['auth'] = "Invalid username or password."
            return render(request, 'module_users/signin.html', {'errors': errors, 'form_data': request.POST})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('module_pages:home')

@login_required
def profile_view(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tenant':
        return HttpResponseForbidden('Only tenants can view this page.')
    return render(request, 'users_module/profile_view.html', {'user_obj': request.user})

@login_required
def profile_edit_view(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tenant':
        return HttpResponseForbidden('Only tenants can edit this page.')
    if request.method == 'POST':
        form = TenantProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('module_users:profile_view')
    else:
        form = TenantProfileForm(instance=request.user)
    return render(request, 'users_module/profile_edit.html', {'form': form})