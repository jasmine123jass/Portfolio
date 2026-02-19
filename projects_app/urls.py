from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
    path('create/', views.project_create, name='project_create'),
    path('<slug:slug>/update/', views.project_update, name='project_update'),
    path('<slug:slug>/delete/', views.project_delete, name='project_delete'),
     path('certificates/', views.certificate_list, name='certificate_list'),
]