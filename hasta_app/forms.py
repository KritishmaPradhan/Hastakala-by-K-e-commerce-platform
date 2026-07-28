from django import forms

from .models import Product, Order


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'price',
            'stock_quantity',
            'category',
            'material',
            'color',
            'size',
            'handmade',
            'customizable',
            'is_featured',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'material': forms.TextInput(attrs={'class': 'form-input'}),
            'color': forms.TextInput(attrs={'class': 'form-input'}),
            'size': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-input'}),
        }
