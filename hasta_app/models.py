from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class UserProfile(models.Model):
    """Extended user profile for Hastakala by K"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Product(models.Model):
    """Product/Gallery model for Hastakala by K handmade crochet items"""
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Product name")
    description = models.TextField(help_text="Detailed product description")
    image_path = models.CharField(max_length=300, help_text="Path to product image (e.g., 'images/gallery12.jpeg')")
    
    # Pricing and Inventory
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)
    stock_quantity = models.PositiveIntegerField(default=1, help_text="Available stock units")
    
    # Ratings and Reviews
    average_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Average rating from 0 to 5 stars"
    )
    total_reviews = models.PositiveIntegerField(default=0, help_text="Number of reviews/ratings")
    
    # Category and Tags
    category = models.CharField(
        max_length=100,
        choices=[
            ('clip', 'Hair Clip'),
            ('keyring', 'Keyring'),
            ('flower', 'Flower'),
            ('toy', 'Toy'),
            ('other', 'Other'),
        ],
        default='other',
        help_text="Product category"
    )
    
    # Additional Attributes
    material = models.CharField(max_length=100, blank=True, default='Yarn', help_text="Material used (e.g., Yarn, Cotton)")
    color = models.CharField(max_length=100, blank=True, help_text="Primary color of the product")
    size = models.CharField(max_length=50, blank=True, help_text="Product size (e.g., Small, Medium, Large)")
    handmade = models.BooleanField(default=True, help_text="Is this product handmade?")
    customizable = models.BooleanField(default=False, help_text="Can this product be customized?")
    
    # Status and Metadata
    is_featured = models.BooleanField(default=False, help_text="Feature this product on homepage")
    is_active = models.BooleanField(default=True, help_text="Is this product available for sale?")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
