from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Store(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    low_stock_quantity = models.PositiveIntegerField(default=5)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_low_stock(self):
        return self.quantity < self.low_stock_quantity

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('SALE', 'Sale'),
        ('PURCHASE', 'Purchase'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.PositiveIntegerField(default=1)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.transaction_type} - {self.product.title} ({self.quantity})"