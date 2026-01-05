from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('login_page/', views.login_view, name='login_page'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('home_page/', views.home_page, name='home_page'),
    path('about_me/', views.about_me, name='about_me'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact_me/', views.contact_me, name='contact_me'),
    path('send_message/', views.send_message, name='send_message'),
    path('email_template_user/', views.email_template_user, name='email_template_user'),
    path('home_searchLoadPortfolioLists/', views.home_searchLoadPortfolioLists, name='home_searchLoadPortfolioLists'),
    path('portfolio_overview/', views.portfolio_overview, name='portfolio_overview'),

    path('portfolio_dashboard/', views.portfolio_dashboard, name='portfolio_dashboard'),
    path('admin_portfolio/', views.admin_portfolio, name='admin_portfolio'),
    path('admin_addPortfolio/', views.admin_addPortfolio, name='admin_addPortfolio'),
    path('admin_portfolio_overview/<portfolio_id>', views.admin_portfolio_overview, name='admin_portfolio_overview'),

    path('admin_addPortfolioFeature/', views.admin_addPortfolioFeature, name='admin_addPortfolioFeature'),
    path('admin_searchLoadPortfolioFeatureLists/', views.admin_searchLoadPortfolioFeatureLists, name='admin_searchLoadPortfolioFeatureLists'),
    path('admin_deletePortfolioFeatureInfo/', views.admin_deletePortfolioFeatureInfo, name='admin_deletePortfolioFeatureInfo'),
    path('admin_portfolio_feature_gallery/<feature_id>', views.admin_portfolio_feature_gallery, name='admin_portfolio_feature_gallery'),
    
    path('admin_searchLoadPortfolioLists/', views.admin_searchLoadPortfolioLists, name='admin_searchLoadPortfolioLists'),
    path('admin_deletePortfolioInfo/', views.admin_deletePortfolioInfo, name='admin_deletePortfolioInfo'),

    
    path('home_searchLoadPortfolioLists/', views.home_searchLoadPortfolioLists, name='home_searchLoadPortfolioLists'),
    path('home_portfolio_overview/<portfolio_id>', views.home_portfolio_overview, name='home_portfolio_overview'),
    path('home_searchLoadPortfolioFeatureLists/', views.home_searchLoadPortfolioFeatureLists, name='home_searchLoadPortfolioFeatureLists'),
    path('home_portfolio_feature_gallery/<feature_id>', views.home_portfolio_feature_gallery, name='home_portfolio_feature_gallery'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)