from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import json

from .models import UserProfile, Product


def home(request):
    """Home page view with all sections"""
    # Fetch active products from database
    products = Product.objects.filter(is_active=True).order_by('created_at')
    # Fetch featured products for carousel
    featured_products = Product.objects.filter(is_featured=True, is_active=True).order_by('created_at')
    
    context = {
        'motto': 'Loops of love in every stitch',
        'about_intro': 'Welcome to Hastakala by K, where every stitch tells a story of love and creativity. Founded by Kritishma Pradhan, our passion is to create beautiful, handmade crochet items that bring warmth and joy to your life.',
        'about_description': 'Each piece is carefully crafted with attention to detail and made with high-quality yarns to ensure durability and comfort.',
        'products': products,
        'featured_products': featured_products,
        'owner_email': 'pradhankritishma@gmail.com',
    }
    return render(request, 'store/index.html', context)


@require_http_methods(["GET"])
def api_carousel_items(request):
    """API endpoint that returns featured products for carousel"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True).order_by('created_at')
    
    items = [
        {
            'image': f'/static/{product.image_path}',
            'title': product.name,
            'description': product.description,
        }
        for product in featured_products
    ]
    
    return JsonResponse({'items': items})


def login(request):
    """Login page view with authentication"""
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('hasta_app:home')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'store/login.html')
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
            # Authenticate with username
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('hasta_app:home')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'store/login.html')


def signup(request):
    """Signup page view with user registration"""
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('hasta_app:home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        terms = request.POST.get('terms', '')
        
        # Validation
        if not all([full_name, email, password, confirm_password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'store/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/signup.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'store/signup.html')
        
        if not terms:
            messages.error(request, 'You must agree to the Terms and Conditions.')
            return render(request, 'store/signup.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'store/signup.html')
        
        try:
            # Create username from email
            username = email.split('@')[0]
            # Handle duplicate usernames
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Parse full name into first and last name
            name_parts = full_name.split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.save()
            
            # Create user profile
            profile = UserProfile.objects.create(user=user, phone_number=phone)
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('hasta_app:login')
        
        except IntegrityError:
            messages.error(request, 'An error occurred. Please try again.')
            return render(request, 'store/signup.html')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return render(request, 'store/signup.html')
    
    return render(request, 'store/signup.html')


def logout(request):
    """Logout view"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('hasta_app:home')
