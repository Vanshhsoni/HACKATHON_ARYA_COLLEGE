# forms.py - Update ProductForm
from django import forms
from .models import Store, Product

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Store Name'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'quantity', 'low_stock_quantity', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'low_stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'Product Name',
            'price': 'Price ($)',
            'quantity': 'Initial Quantity',
            'low_stock_quantity': 'Low Stock Threshold',
            'image': 'Product Image'
        }
        help_texts = {
            'low_stock_quantity': 'Alert will appear when quantity falls below this value'
        }