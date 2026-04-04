from django.contrib import admin
from .models import UserProfile

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
