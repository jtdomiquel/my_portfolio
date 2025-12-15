from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')  
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:

                login(request, user)
                return redirect('portfolio_dashboard')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Both username and password are required.')
    
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        
        firstname = request.POST.get('first_name')
        middlename = request.POST.get('middle_name')
        lastname = request.POST.get('last_name')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if not username or not password or not confirm_password:
            messages.error(request, 'Username, password, and confirm password are required.')
            return render(request, 'sign_up.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'sign_up.html')

        if UserInfo.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return render(request, 'sign_up.html')

        try:
        
            user = UserInfo(
                firstname=firstname,
                middlename=middlename,
                lastname=lastname,
                contact_no=contact_no,
                address=address,
                username=username,
                password=make_password(password),
                is_active=False,
            )
            
            user.save()

            messages.success(request, 'Account created successfully.')
            return redirect('login_page')
        
        except ValidationError as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'sign_up.html')

    return render(request, 'sign_up.html')

def home_page(request):
    return render(request, 'home_page.html')

def about_me(request):
    return render(request, 'about_me.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def portfolio_dashboard(request):
    return render(request, 'base_template_dashboard.html')


    
