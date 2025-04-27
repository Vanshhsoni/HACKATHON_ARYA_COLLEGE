from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import F, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Store, Product, Transaction
from .forms import StoreForm, ProductForm

@login_required
def home(request):
    stores = Store.objects.filter(user=request.user)
    store_form = StoreForm()
    
    # Calculate stats
    total_products = Product.objects.filter(store__user=request.user).count()
    
    # Count products with low stock
    low_stock_count = Product.objects.filter(
        store__user=request.user,
        quantity__lt=F('low_stock_quantity')
    ).count()
    
    # Get sales and purchase stats for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    sales = Transaction.objects.filter(
        product__store__user=request.user,
        transaction_type='SALE',
        timestamp__gte=thirty_days_ago
    ).aggregate(
        total_count=Sum('quantity'),
        total_amount=Sum('total_amount')
    )
    
    purchases = Transaction.objects.filter(
        product__store__user=request.user,
        transaction_type='PURCHASE',
        timestamp__gte=thirty_days_ago
    ).aggregate(
        total_count=Sum('quantity'),
        total_amount=Sum('total_amount')
    )
    
    context = {
        'stores': stores,
        'store_form': store_form,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'sales': sales,
        'purchases': purchases,
    }
    return render(request, 'inventory/home.html', context)

@login_required
def create_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.user = request.user
            store.save()
            return redirect('inventory:store_detail', store_id=store.id)
    
    return redirect('inventory:home')

@login_required
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id, user=request.user)
    products = store.products.all()
    product_form = ProductForm()
    
    # Get sales and purchase stats for this store
    thirty_days_ago = timezone.now() - timedelta(days=30)
    sales = Transaction.objects.filter(
        product__store=store,
        transaction_type='SALE',
        timestamp__gte=thirty_days_ago
    ).aggregate(
        total_count=Sum('quantity'),
        total_amount=Sum('total_amount')
    )
    
    purchases = Transaction.objects.filter(
        product__store=store,
        transaction_type='PURCHASE',
        timestamp__gte=thirty_days_ago
    ).aggregate(
        total_count=Sum('quantity'),
        total_amount=Sum('total_amount')
    )
    
    context = {
        'store': store,
        'products': products,
        'product_form': product_form,
        'sales': sales,
        'purchases': purchases,
    }
    return render(request, 'inventory/store_detail.html', context)

@login_required
def create_product(request, store_id):
    store = get_object_or_404(Store, id=store_id, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('inventory:store_detail', store_id=store.id)
    
    return redirect('inventory:store_detail', store_id=store.id)

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:store_detail', store_id=product.store.id)
    
    return redirect('inventory:store_detail', store_id=product.store.id)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__user=request.user)
    store_id = product.store.id
    product.delete()
    
    return redirect('inventory:store_detail', store_id=store_id)

@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, user=request.user)
    store.delete()
    return redirect('inventory:home')

@login_required
def get_store_products(request, store_id):
    store = get_object_or_404(Store, id=store_id, user=request.user)
    products = list(store.products.values('id', 'title', 'price', 'quantity'))
    return JsonResponse({'products': products})

@login_required
def record_transaction(request, store_id):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        transaction_type = request.POST.get('transaction_type')
        
        product = get_object_or_404(Product, id=product_id, store__user=request.user)
        
        if transaction_type == 'SALE':
            # For sales, we need to ensure there's enough stock
            if product.quantity < quantity:
                return JsonResponse({
                    'success': False, 
                    'message': f'Not enough stock. Available: {product.quantity}'
                })
            
            # Decrease product quantity for sales
            product.quantity -= quantity
            # Calculate total amount for the sale
            total_amount = product.price * quantity
            
        elif transaction_type == 'PURCHASE':
            # Increase product quantity for purchases
            product.quantity += quantity
            # Calculate total amount for the purchase
            total_amount = product.price * quantity
        
        # Save the updated product quantity
        product.save()
        
        # Create a transaction record
        Transaction.objects.create(
            product=product,
            quantity=quantity,
            transaction_type=transaction_type,
            total_amount=total_amount
        )
        
        return JsonResponse({
            'success': True, 
            'new_quantity': product.quantity,
            'is_low_stock': product.is_low_stock
        })
        
    return JsonResponse({'success': False, 'message': 'Invalid request'})