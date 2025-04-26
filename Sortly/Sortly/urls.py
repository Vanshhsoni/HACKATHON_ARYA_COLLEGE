from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('accounts:index'), name='root'),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
]