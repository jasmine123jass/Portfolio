from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Project URLs
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
    path('<slug:slug>/update/', views.project_update, name='project_update'),
    path('<slug:slug>/delete/', views.project_delete, name='project_delete'),
    
    # Certificate URLs
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/create/', views.certificate_create, name='certificate_create'),
    path('certificates/<int:pk>/update/', views.certificate_update, name='certificate_update'),
    path('certificates/<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
]