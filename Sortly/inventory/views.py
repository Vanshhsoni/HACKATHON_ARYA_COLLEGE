from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Home page for authenticated users"""
    return render(request, 'inventory/home.html')

# Add login_required decorator to all views that should be protected