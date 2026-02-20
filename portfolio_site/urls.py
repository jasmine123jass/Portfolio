from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from projects_app import views as project_views
from accounts_app import views as accounts_views

# Admin site requires login and staff status
admin.site.login = login_required(admin.site.login, login_url='accounts:admin_login')

urlpatterns = [
    # Admin login (separate - only for you)
    path('admin/login/', accounts_views.admin_login_view, name='admin_login'),
    path('admin/', admin.site.urls),  # Admin panel
    
    # User login (portfolio - only for you)
    path('login/', accounts_views.login_view, name='login'),
    path('', accounts_views.login_view, name='root_login'),  # Root redirects to login
    
    # Portfolio (requires login)
    path('home/', project_views.home, name='home'),
    path('projects/', include('projects_app.urls')),
    path('certificates/', project_views.certificate_list, name='certificate_list'),
    path('contact/', include('contact_app.urls')),
    path('accounts/', include('accounts_app.urls')),
    path('api/', include('api_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)