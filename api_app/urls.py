from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('projects/', views.ProjectListAPI.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailAPI.as_view(), name='project-detail'),
    path('contact/', views.ContactCreateAPI.as_view(), name='contact-create'),
    path('token/', views.CustomAuthToken.as_view(), name='token'),
]
