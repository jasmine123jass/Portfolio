# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache
# from projects_app import views as project_views
# from accounts_app import views as accounts_views
# from contact_app import views as contact_views
# from certificates_app import views as certificate_views

# # Admin site requires login and staff status
# admin.site.login = never_cache(login_required(admin.site.login, login_url='admin_portal_login'))

# urlpatterns = [
#     # ===== ADMIN PORTAL (Completely Separate) =====
#     # Admin Portal Login - Unique design, no navbar
#     path('admin/login', accounts_views.admin_portal_login, name='admin_portal_login'),
    
#     # Admin Panel - Direct to Django admin (NO CUSTOM DASHBOARD)
#     path('dashboard/', admin.site.urls, name='admin_panel'),
#     # path('adminl/',admin.django.contrib.admin.site.urls, name='admin_panel'),  # <-- ADMIN PANEL (Django Admin)
    
#     # ===== PUBLIC PORTFOLIO (NO LOGIN REQUIRED) =====
#     # Public home page - Shows projects and certificates
#     path('', accounts_views.home_view, name='home'),  # <-- PUBLIC HOME PAGE
#     path('admin/', admin.site.urls), 
    
#     # Public project listing
#     path('projects/', include('projects_app.urls')),  # <-- PUBLIC PROJECTS
    
#     # Public certificates listing
#     path('certificates/', certificate_views.certificate_list, name='certificate_list'),  # <-- PUBLIC CERTIFICATES
    
#     # Public contact page
#     path('contact/', include('contact_app.urls')),  # <-- PUBLIC CONTACT
    
#     # ===== AUTHENTICATION URLs =====
#     # Login page (only for admin/staff)
#     path('login/', accounts_views.login_view, name='login'),
    
#     # Logout
#     path('logout/', accounts_views.logout_view, name='logout'),
    
#     # Signup (disabled - redirects to home)
#     path('signup/', accounts_views.signup_view, name='signup'),
    
#     # ===== PROTECTED PAGES (LOGIN REQUIRED) =====
#     # User dashboard - only for authorized users
#     path('dashboard/', accounts_views.dashboard, name='dashboard'),
    
#     # ===== USER ACCOUNTS (includes management views) =====
#     path('accounts/', include('accounts_app.urls')),
    
#     # ===== API ENDPOINTS =====
#     path('api/', include('api_app.urls')),
# ]

# # Serve static and media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # Custom error pages (optional)
# handler404 = 'portfolio_site.views.custom_404'
# handler500 = 'portfolio_site.views.custom_500'

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from projects_app import views as project_views
from accounts_app import views as accounts_views
from contact_app import views as contact_views

urlpatterns = [
    # ===== ADMIN PANEL (Protected) =====
    # Django admin - requires staff login
    # Admin portal login alias (exposed as top-level name 'admin_portal_login')
    path('admin/login', accounts_views.admin_portal_login, name='admin_portal_login'),
    path('admin/', admin.site.urls),
    
    # ===== PUBLIC PORTFOLIO (No Login Required) =====
    # Home page
    path('', project_views.home, name='home'),
    
    # Projects listing
    path('projects/', include('projects_app.urls')),
    
    # Certificates listing
    path('certificates/', project_views.certificate_list, name='certificate_list'),
    
    # Contact page
    path('contact/', include('contact_app.urls')),
    
    # User dashboard (login-protected view in `accounts_app`)
    path('dashboard/', accounts_views.dashboard, name='dashboard'),

    # Authentication aliases (top-level names expected by templates/views)
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('signup/', accounts_views.signup_view, name='signup'),
    
    # ===== API ENDPOINTS =====
    path('api/', include('api_app.urls')),
    
    # ===== OPTIONAL: Authentication (if needed later) =====
    # Login page (commented out - not needed for public site)
    # path('login/', accounts_views.login_view, name='login'),
    
    # Logout (commented out)
    # path('logout/', accounts_views.logout_view, name='logout'),

    # Accounts app (register with namespace so templates can reverse 'accounts:...')
    path('accounts/', include(('accounts_app.urls', 'accounts'), namespace='accounts')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error pages (optional)
handler404 = 'portfolio_site.views.custom_404'
handler500 = 'portfolio_site.views.custom_500'