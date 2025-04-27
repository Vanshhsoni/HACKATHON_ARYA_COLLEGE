from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='home'),
    path('store/create/', views.create_store, name='create_store'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('store/<int:store_id>/create-product/', views.create_product, name='create_product'),
    path('product/<int:product_id>/update/', views.update_product, name='update_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('store/<int:store_id>/delete/', views.delete_store, name='delete_store'),
    path('store/<int:store_id>/products/', views.get_store_products, name='get_store_products'),
    # Add this to your urlpatterns in urls.py
path('store/<int:store_id>/transaction/', views.record_transaction, name='record_transaction'),
]