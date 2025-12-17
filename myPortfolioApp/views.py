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

def portfolio_overview(request):
    return render(request, 'portfolio_overview.html')

def portfolio_dashboard(request):
    return render(request, 'base_template_dashboard.html')

@login_required
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

def home_searchLoadPortfolioLists(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)


    if query:
        filter_conditions = Q()
        if query:
            filter_conditions |= Q(project_title__icontains=query) | \
                                 Q(priority__icontains=query) | \
                                 Q(status__icontains=query) | \
                                 Q(skills__icontains=query) 
        
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

@login_required
def admin_portfolio_overview(request, portfolio_id):

    portfolioDetails = portfolio_details.objects.get(id=int(portfolio_id))
    
    portfolioDetailsList = {
        'portfolio_id': portfolioDetails.id,
        'project_title': portfolioDetails.project_title if portfolioDetails.project_title else "",
        'project_thumbnail': portfolioDetails.thumbnail_image if portfolioDetails.thumbnail_image else None,
        'project_discriptions': portfolioDetails.project_discriptions if portfolioDetails.project_discriptions else "",
        'priority': portfolioDetails.priority if portfolioDetails.priority else "",
        'status': portfolioDetails.status if portfolioDetails.status else "",
        'skills': portfolioDetails.skills.split(', ') if portfolioDetails.skills else [],
        'date_finished': portfolioDetails.date_finished.strftime("%b. %d, %Y") if portfolioDetails.date_finished else "",
        'date_save': portfolioDetails.date_save.strftime("%b. %d, %Y") if portfolioDetails.date_save else "",
    }
    
    return render(request, 'admin_portfolio_overview.html', {
        'portfolioDetailsList' : portfolioDetailsList,
        })

@login_required
def admin_addPortfolioFeature(request):
    if request.method == 'POST':
        portfolio_id = request.POST.get('portfolioId')
        portfolioDetails = portfolio_details.objects.get(id=int(portfolio_id))

        feature_title = request.POST.get('featureTitle')
        thumbnail_image = request.FILES.get('thumbnailFile')
        feature_description = request.POST.get('featureDescription')
        feature_priority = request.POST.get('featurePriority')
        feature_status = request.POST.get('featureStatus')
        feature_skills = request.POST.get('featureUseSkills')
        feature_due_date = request.POST.get('featureDueDate')
        
        feature_files = request.FILES.getlist('featureFiles')

        user = request.user

        portfolioFeatureDetails = portfolio_features.objects.create(
            feature_user_id=user,
            feature_portfolio_id=portfolioDetails,
            feature_title=feature_title,
            thumbnail_image=thumbnail_image,
            feature_discriptions=feature_description,
            priority=feature_priority,
            status=feature_status,
            skills=feature_skills,
            date_finished=feature_due_date,
        )

        for file in feature_files:
            portfolio_features_files.objects.create(portfolio_feat_id=portfolioFeatureDetails, picture_path=file)
        
        messages.success(request, 'Done.')
        return redirect('admin_portfolio_overview', portfolio_id)

    messages.error(request, 'Item not found!')
    return redirect('admin_portfolio_overview', portfolio_id)

@login_required
def admin_searchLoadPortfolioFeatureLists(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    portfolio_id = request.GET.get('portfolio_id')

    user = request.user

    if query:
        filter_conditions = Q()
        if query:
            filter_conditions |= Q(feature_title__icontains=query) | \
                                 Q(priority__icontains=query) | \
                                 Q(status__icontains=query) | \
                                 Q(skills__icontains=query) | \
                                 Q(feature_discriptions__icontains=query) 
        
        filter_conditions &= Q(feature_user_id=user.id) 
        filter_conditions &= Q(feature_portfolio_id=portfolio_id) 
        
        portfolioFeatureDetailLists = portfolio_features.objects.filter(filter_conditions).order_by('-date_finished')
    else:
        portfolioFeatureDetailLists = portfolio_features.objects.all().order_by('-date_finished')
    

    paginator = Paginator(portfolioFeatureDetailLists, 8) 
    try:
        models_page = paginator.page(page)
    except PageNotAnInteger:
        models_page = paginator.page(1)
    except EmptyPage:
        models_page = []

    data = []
    for feature in models_page:
        data.append({
            'feature_id': feature.id,
            'feature_title': feature.feature_title if feature.feature_title else "",
            'thumbnail_image':request.build_absolute_uri(settings.MEDIA_URL + str(feature.thumbnail_image)) if feature.thumbnail_image else '',
            'feature_discriptions': feature.feature_discriptions if feature.feature_discriptions else "",
            'priority': feature.priority if feature.priority else "",
            'status': feature.status if feature.status else "",
            'skills': feature.skills if feature.skills else "",
            'date_finished': feature.date_finished.strftime("%b. %d, %Y") if feature.date_finished else "",
        })

    return JsonResponse({
        'portfolioDataLists': data,
        'current_page': models_page.number if models_page else 1,
        'total_pages': paginator.num_pages if paginator.count > 0 else 1
    })

@login_required
def admin_deletePortfolioFeatureInfo(request):
    try:
        portfolioFeatureId = request.POST.get('deletePortfolioFeature_id')
        portfolio_id = request.POST.get('deletePortfolio_id')

        portfolioFeatureDetails = portfolio_features.objects.get(id=portfolioFeatureId)

        thumbnail_path = portfolioFeatureDetails.thumbnail_image.path if portfolioFeatureDetails.thumbnail_image else None
        related_files = portfolio_features_files.objects.filter(portfolio_feat_id=portfolioFeatureDetails)

        for file_obj in related_files:
            if file_obj.picture_path:
                # Delete the actual file from storage
                if os.path.exists(file_obj.picture_path.path):
                    default_storage.delete(file_obj.picture_path.path)
            # Delete the database record
            file_obj.delete()
        
        if thumbnail_path and os.path.exists(thumbnail_path):
            default_storage.delete(thumbnail_path)
        
        portfolioFeatureDetails.delete()
        messages.success(request, 'Portfolio and all related files deleted successfully!')
        
        return redirect('admin_portfolio_overview', portfolio_id)

    except portfolioFeatureDetails.DoesNotExist:
        messages.error(request, 'Item not found!')
        return redirect('admin_portfolio_overview', portfolio_id)