from django.contrib import admin
from .models import UserProfile, Product, Wishlist, Cart, CartItem

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


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('products',)
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Products', {'fields': ('products',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products in Wishlist'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'total_price_display', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items in Cart'
    
    def total_price_display(self, obj):
        return f"₹{obj.get_total_price()}"
    total_price_display.short_description = 'Total Price'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at', 'updated_at')
    fields = ('product', 'quantity', 'added_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_item_total', 'added_at')
    list_filter = ('added_at', 'updated_at')
    search_fields = ('cart__user__email', 'product__name')
    readonly_fields = ('added_at', 'updated_at', 'get_item_total')
    
    def get_item_total(self, obj):
        return f"₹{obj.get_item_total()}"
    get_item_total.short_description = 'Item Total'
