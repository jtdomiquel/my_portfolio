from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('login_page/', views.login_view, name='login_page'),
    path('signup/', views.signup, name='signup'),
    path('home_page/', views.home_page, name='home_page'),
    path('about_me/', views.about_me, name='about_me'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio_dashboard/', views.portfolio_dashboard, name='portfolio_dashboard'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)