# inventory/urls.py
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('/', views.home, name='home'),
    path('store/create/', views.create_store, name='create_store'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('store/<int:store_id>/product/create/', views.create_product, name='create_product'),
    path('product/<int:product_id>/update/', views.update_product, name='update_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]