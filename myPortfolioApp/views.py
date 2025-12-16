from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q

from django.db import transaction
from django.core.files.storage import default_storage
import os

def login_view(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')  
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:

                login(request, user)
                return redirect('admin_portfolio')

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

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home_page')

def home_page(request):
    return render(request, 'home_page.html')

def about_me(request):
    return render(request, 'about_me.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def portfolio_dashboard(request):
    return render(request, 'base_template_dashboard.html')

def admin_portfolio(request):
    return render(request, 'admin_portfolio.html')

@login_required
def admin_addPortfolio(request):
    if request.method == 'POST':
        project_title = request.POST.get('projectTitle')
        thumbnail_image = request.FILES.get('thumbnailFile')
        project_description = request.POST.get('projectDescription')
        project_priority = request.POST.get('projectPriority')
        project_status = request.POST.get('projectStatus')
        project_due_date = request.POST.get('projectDueDate')
        project_skills = request.POST.get('projectUseSkills')
        
        project_files = request.FILES.getlist('projectFiles')

        user = request.user

        portfolioDetails = portfolio_details.objects.create(
            user_id=user,
            project_title=project_title,
            thumbnail_image=thumbnail_image,
            project_discriptions=project_description,
            priority=project_priority,
            status=project_status,
            skills=project_skills,
            date_finished=project_due_date,
        )

        for file in project_files:
            portfolio_files.objects.create(portfolio_id=portfolioDetails, picture_path=file)
        
        messages.success(request, 'Done.')
        return redirect('admin_portfolio')

    messages.error(request, 'Item not found!')
    return redirect('admin_portfolio')

@login_required
def admin_searchLoadPortfolioLists(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    user = request.user

    if query:
        filter_conditions = Q()
        if query:
            filter_conditions |= Q(project_title__icontains=query) | \
                                 Q(priority__icontains=query) | \
                                 Q(status__icontains=query) | \
                                 Q(skills__icontains=query) 
        
        filter_conditions &= Q(user_id=user.id) 
        
        portfolioDetailLists = portfolio_details.objects.filter(filter_conditions).order_by('-date_finished')
    else:
        portfolioDetailLists = portfolio_details.objects.all().order_by('-date_finished')
    

    paginator = Paginator(portfolioDetailLists, 8) 
    try:
        models_page = paginator.page(page)
    except PageNotAnInteger:
        models_page = paginator.page(1)
    except EmptyPage:
        models_page = []

    data = []
    for portfolio in models_page:
        data.append({
            'portfolio_id': portfolio.id,
            'project_title': portfolio.project_title if portfolio.project_title else "",
            'thumbnail_image':request.build_absolute_uri(settings.MEDIA_URL + str(portfolio.thumbnail_image)) if portfolio.thumbnail_image else '',
            'project_discriptions': portfolio.project_discriptions if portfolio.project_discriptions else "",
            'priority': portfolio.priority if portfolio.priority else "",
            'status': portfolio.status if portfolio.status else "",
            'skills': portfolio.skills if portfolio.skills else "",
            'date_finished': portfolio.date_finished.strftime("%b. %d, %Y") if portfolio.date_finished else "",
        })

    return JsonResponse({
        'portfolioDataLists': data,
        'current_page': models_page.number if models_page else 1,
        'total_pages': paginator.num_pages if paginator.count > 0 else 1
    })

@login_required
def admin_deletePortfolioInfo(request):
    try:
        portfolioId = request.POST.get('deletePortfolio_id')

        portfolioDetails = portfolio_details.objects.get(id=portfolioId)

        thumbnail_path = portfolioDetails.thumbnail_image.path if portfolioDetails.thumbnail_image else None
        related_files = portfolio_files.objects.filter(portfolio_id=portfolioDetails)

        for file_obj in related_files:
            if file_obj.picture_path:
                # Delete the actual file from storage
                if os.path.exists(file_obj.picture_path.path):
                    default_storage.delete(file_obj.picture_path.path)
            # Delete the database record
            file_obj.delete()
        
        if thumbnail_path and os.path.exists(thumbnail_path):
            default_storage.delete(thumbnail_path)
        
        portfolioDetails.delete()
        messages.success(request, 'Portfolio and all related files deleted successfully!')
        
        return redirect('admin_portfolio')

    except portfolioDetails.DoesNotExist:
        messages.error(request, 'Item not found!')
        return redirect('admin_portfolio')