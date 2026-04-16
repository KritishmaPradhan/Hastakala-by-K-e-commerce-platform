from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import json

from .models import UserProfile, Product, Wishlist, Cart, CartItem


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


def product_detail(request, product_id):
    """Product detail page view"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('hasta_app:home')
    
    # Get related products (same category)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


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
    # If already logged in, redirect appropriately
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('hasta_app:home')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', '')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'store/login.html', {'next': next_url})
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
            # Authenticate with username
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                # Redirect to next URL if provided, otherwise home
                if next_url:
                    return redirect(next_url)
                return redirect('hasta_app:home')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    
    next_url = request.GET.get('next', '')
    context = {'next': next_url}
    return render(request, 'store/login.html', context)


def signup(request):
    """Signup page view with user registration"""
    # If already logged in, redirect appropriately
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('hasta_app:home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        terms = request.POST.get('terms', '')
        next_url = request.POST.get('next', '')
        
        # Validation
        if not all([full_name, email, password, confirm_password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'store/signup.html', {'next': next_url})
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/signup.html', {'next': next_url})
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'store/signup.html', {'next': next_url})
        
        if not terms:
            messages.error(request, 'You must agree to the Terms and Conditions.')
            return render(request, 'store/signup.html', {'next': next_url})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'store/signup.html', {'next': next_url})
        
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
            
            # Auto-login the user after signup
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome {user.first_name or user.username}! Account created successfully.')
                # Redirect to next URL if provided, otherwise home
                if next_url:
                    return redirect(next_url)
                return redirect('hasta_app:home')
        
        except IntegrityError:
            messages.error(request, 'An error occurred. Please try again.')
            return render(request, 'store/signup.html', {'next': next_url})
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return render(request, 'store/signup.html', {'next': next_url})
    
    next_url = request.GET.get('next', '')
    context = {'next': next_url}
    return render(request, 'store/signup.html', context)


def logout(request):
    """Logout view"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('hasta_app:home')


@login_required(login_url='hasta_app:login')
def wishlist_page(request):
    """Wishlist page view - displays all wishlisted items"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlisted_products = wishlist.products.filter(is_active=True)
    
    context = {
        'wishlisted_products': wishlisted_products,
    }
    return render(request, 'store/wishlist.html', context)


@require_http_methods(["POST"])
@login_required(login_url='hasta_app:login')
def toggle_wishlist(request):
    """AJAX endpoint to add/remove product from wishlist"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'})
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
        
        # Get or create user's wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        # Check if product is already wishlisted
        is_wishlisted = wishlist.is_product_wishlisted(product)
        
        if is_wishlisted:
            wishlist.remove_product(product)
            return JsonResponse({
                'success': True,
                'action': 'removed',
                'message': f'{product.name} removed from wishlist'
            })
        else:
            wishlist.add_product(product)
            return JsonResponse({
                'success': True,
                'action': 'added',
                'message': f'{product.name} added to wishlist'
            })
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


@require_http_methods(["GET"])
@login_required(login_url='hasta_app:login')
def check_wishlist(request, product_id):
    """AJAX endpoint to check if product is in user's wishlist"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        is_wishlisted = wishlist.is_product_wishlisted(product)
        
        return JsonResponse({
            'success': True,
            'is_wishlisted': is_wishlisted
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


@login_required(login_url='hasta_app:login')
def cart_page(request):
    """Cart page view - displays all cart items"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.get_total_price()
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': cart.get_total_items(),
    }
    return render(request, 'store/cart.html', context)


@require_http_methods(["POST"])
@login_required(login_url='hasta_app:login')
def add_to_cart(request):
    """AJAX endpoint to add product to cart"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if not product_id or quantity <= 0:
            return JsonResponse({'success': False, 'message': 'Invalid product ID or quantity'})
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
        
        if quantity > product.stock_quantity:
            return JsonResponse({'success': False, 'message': f'Only {product.stock_quantity} items available'})
        
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Add product to cart
        cart_item, item_created = cart.items.get_or_create(product=product)
        if not item_created:
            if cart_item.quantity + quantity > product.stock_quantity:
                return JsonResponse({'success': False, 'message': f'Only {product.stock_quantity} items available'})
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'total_items': cart.get_total_items(),
            'total_price': float(cart.get_total_price()),
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


@require_http_methods(["POST"])
@login_required(login_url='hasta_app:login')
def remove_from_cart(request):
    """AJAX endpoint to remove product from cart"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'})
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
        
        cart = Cart.objects.get(user=request.user)
        cart.remove_product(product)
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} removed from cart',
            'total_items': cart.get_total_items(),
            'total_price': float(cart.get_total_price()),
        })
    
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


@require_http_methods(["POST"])
@login_required(login_url='hasta_app:login')
def update_cart_item(request):
    """AJAX endpoint to update quantity of an item in cart"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 0))
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'})
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
        
        cart = Cart.objects.get(user=request.user)
        
        if quantity <= 0:
            cart.remove_product(product)
            return JsonResponse({
                'success': True,
                'message': f'{product.name} removed from cart',
                'total_items': cart.get_total_items(),
                'total_price': float(cart.get_total_price()),
            })
        
        if quantity > product.stock_quantity:
            return JsonResponse({'success': False, 'message': f'Only {product.stock_quantity} items available'})
        
        cart.update_quantity(product, quantity)
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'total_items': cart.get_total_items(),
            'total_price': float(cart.get_total_price()),
        })
    
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


@require_http_methods(["GET"])
@login_required(login_url='hasta_app:login')
def get_cart_info(request):
    """AJAX endpoint to get cart information"""
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        return JsonResponse({
            'success': True,
            'total_items': cart.get_total_items(),
            'total_price': float(cart.get_total_price()),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
