from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from .models import Property, PropertyRating, PropertyRequest
from .forms import PropertyForm, PropertyRatingForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.

def property_map_view(request):
    return render(request, 'property_module/property_map.html')

def property_list_json(request):
    properties = Property.objects.all()
    data = [
        {
            'id': prop.id,
            'title': prop.title,
            'address': prop.address,
            'latitude': prop.latitude,
            'longitude': prop.longitude,
            'rental_price': str(prop.rental_price),
            'detail_url': reverse('module_property:property_detail', args=[prop.id]),
        }
        for prop in properties
    ]
    return JsonResponse({'properties': data})

@login_required
def add_property_view(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'landlord':
        return HttpResponseForbidden('Only landlords can add properties.')
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.landlord = request.user
            property_obj.save()
            return redirect('module_property:property_map')
    else:
        form = PropertyForm()
    return render(request, 'property_module/add_property.html', {'form': form})

def property_detail_view(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    ratings = property_obj.ratings.select_related('user').all()
    avg_rating = property_obj.average_rating() or 0
    show_review_form = False
    review_form = None
    user_review = None
    show_request_button = False
    request_status = None
    user_property_request = None
    approved_tenants = [req.tenant for req in property_obj.requests.filter(status='approved').select_related('tenant')]
    if request.user.is_authenticated and hasattr(request.user, 'user_type'):
        if request.user.user_type == 'tenant':
            show_review_form = True
            try:
                user_review = property_obj.ratings.get(user=request.user)
            except PropertyRating.DoesNotExist:
                user_review = None
            # PropertyRequest logic
            user_property_request = PropertyRequest.objects.filter(property=property_obj, tenant=request.user).first()
            if not user_property_request:
                show_request_button = True
            else:
                request_status = user_property_request.status
            # Handle review form
            if request.method == 'POST' and 'review_submit' in request.POST:
                form = PropertyRatingForm(request.POST, instance=user_review)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.property = property_obj
                    review.save()
                    messages.success(request, 'Your review has been submitted!')
                    return redirect('module_property:property_detail', pk=property_obj.pk)
                else:
                    review_form = form
            else:
                review_form = PropertyRatingForm(instance=user_review)
        elif request.user.user_type == 'landlord':
            # Landlords do not see request/review forms
            pass
    # Handle property request creation
    if request.method == 'POST' and 'request_submit' in request.POST and show_request_button:
        PropertyRequest.objects.create(property=property_obj, tenant=request.user, status='pending')
        return redirect('module_property:property_detail', pk=property_obj.pk)
    return render(request, 'property_module/property_detail.html', {
        'property': property_obj,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'show_review_form': show_review_form,
        'review_form': review_form,
        'user_review': user_review,
        'show_request_button': show_request_button,
        'request_status': request_status,
        'user_property_request': user_property_request,
        'approved_tenants': approved_tenants,
    })

@login_required
def my_properties_view(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'landlord':
        return HttpResponseForbidden('Only landlords can view this page.')
    properties = Property.objects.filter(landlord=request.user)
    return render(request, 'property_module/my_properties.html', {'properties': properties})

@login_required
def edit_property_view(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, landlord=request.user)
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'landlord':
        return HttpResponseForbidden('Only landlords can edit properties.')
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('module_property:property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'property_module/add_property.html', {
        'form': form,
        'edit_mode': True,
        'property': property_obj,
    })

@login_required
def landlord_requests_view(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'landlord':
        return HttpResponseForbidden('Only landlords can view this page.')
    requests = PropertyRequest.objects.filter(property__landlord=request.user).select_related('property', 'tenant').order_by('-created_at')
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')
        prop_request = get_object_or_404(PropertyRequest, id=req_id, property__landlord=request.user)
        if action == 'approve':
            prop_request.status = 'approved'
            prop_request.save()
        elif action == 'reject':
            prop_request.status = 'declined'
            prop_request.save()
        return redirect('module_property:landlord_requests')
    return render(request, 'property_module/landlord_requests.html', {'requests': requests})
