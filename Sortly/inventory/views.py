# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Store, Product
from .forms import StoreForm, ProductForm

@login_required
def home(request):
    stores = Store.objects.filter(user=request.user)
    store_form = StoreForm()
    
    context = {
        'stores': stores,
        'store_form': store_form,
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
    
    context = {
        'store': store,
        'products': products,
        'product_form': product_form,
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