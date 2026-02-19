from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static,views
from projects_app import views as project_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', project_views.home, name='home'),
    path('projects/', include('projects_app.urls')),
    path('contact/', include('contact_app.urls')),
    path('accounts/', include('accounts_app.urls')),
    path('api/', include('api_app.urls')),
      path('certificates/', views.certificate_list, name='certificate_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)