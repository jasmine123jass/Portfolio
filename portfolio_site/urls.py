from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from projects_app import views as project_views
from accounts_app import views as accounts_views

# Admin site requires login and staff status
admin.site.login = never_cache(login_required(admin.site.login, login_url='admin_portal_login'))

urlpatterns = [
    # ===== ADMIN PORTAL (Completely Separate) =====
    # Admin Portal Login - Unique design, no navbar
    path('admin/login/', accounts_views.admin_portal_login, name='admin_portal_login'),
    
    # Admin Panel - Direct to Django admin (NO CUSTOM DASHBOARD)
    path('admin/', admin.site.urls, name='admin_panel'),
    
    # ===== USER PORTFOLIO =====
    # User login (portfolio - only for authorized users)
    path('login/', accounts_views.login_view, name='login'),
    path('', accounts_views.login_view, name='root_login'),
    
    # Portfolio pages (requires login)
    path('home/', project_views.home, name='home'),
    path('projects/', include('projects_app.urls')),
    path('certificates/', project_views.certificate_list, name='certificate_list'),
    path('contact/', include('contact_app.urls')),
    
    # ===== USER ACCOUNTS =====
    path('accounts/', include('accounts_app.urls')),
    
    # ===== API ENDPOINTS =====
    path('api/', include('api_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)