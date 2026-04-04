from django.contrib import admin
from .models import UserProfile, Product

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'city')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Contact Information', {'fields': ('phone_number', 'address', 'city', 'postal_code')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'average_rating', 'is_active', 'is_featured', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'material', 'handmade', 'customizable', 'created_at')
    search_fields = ('name', 'description', 'color')
    readonly_fields = ('created_at', 'updated_at', 'total_reviews')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image_path')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Ratings & Reviews', {
            'fields': ('average_rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('category', 'material', 'color', 'size')
        }),
        ('Product Attributes', {
            'fields': ('handmade', 'customizable', 'is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
