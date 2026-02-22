from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # User authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Admin portal login (separate)
    path('admin/login/', views.admin_portal_login, name='admin_portal_login'),
    
    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    
    
    # Management views
    path('manage/projects/', views.manage_projects, name='manage_projects'),
    path('manage/certificates/', views.manage_certificates, name='manage_certificates'),
    path('manage/messages/', views.manage_messages, name='manage_messages'),
    
    # Message actions
    path('manage/message/<int:pk>/read/', views.mark_message_read, name='mark_message_read'),
    path('manage/message/<int:pk>/delete/', views.delete_message, name='delete_message'),
    
    # Project CRUD
    path('manage/project/create/', views.project_create, name='project_create'),
    path('manage/project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('manage/project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Certificate CRUD
    path('manage/certificate/create/', views.certificate_create, name='certificate_create'),
    path('manage/certificate/<int:pk>/edit/', views.certificate_edit, name='certificate_edit'),
    path('manage/certificate/<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
]