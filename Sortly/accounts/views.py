from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from inventory import views

def index(request):
    """Landing page with login/signup options"""
    return render(request, 'accounts/index.html')

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, 'accounts/login.html')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('accounts:index')  # 🔥 Redirect to your landing page or homepage
        else:
            messages.error(request, "Invalid login credentials.")
    
    return render(request, 'accounts/login.html')

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('inventory:home')  # Redirect to your landing page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'accounts/login.html')



def signup_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        fullname = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'accounts/signup.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'accounts/signup.html')
        
        # Create the user
        try:
            # Parse full name into first and last name
            name_parts = fullname.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Log the user in immediately
            login(request, user)
            messages.success(request, f"Welcome to Sortly, {user.get_full_name() or user.username}!")
            return redirect('inventory:home')  # Redirect to home page after signup
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
    
    return render(request, 'accounts/signup.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:index')