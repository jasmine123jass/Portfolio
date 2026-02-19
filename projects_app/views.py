from django.shortcuts import render
from .models import Project, Certificate
from accounts_app.models import Profile

def home(request):
    projects = Project.objects.all()[:3]  # Latest 3 projects
    certificates = Certificate.objects.all()[:6]  # Latest 6 certificates
    profile = Profile.objects.first()
    
    context = {
        'projects': projects,
        'certificates': certificates,
        'profile': profile,
    }
    return render(request, 'home.html', context)

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def project_detail(request, slug):
    project = Project.objects.get(slug=slug)
    return render(request, 'project_detail.html', {'project': project})

def certificate_list(request):
    certificates = Certificate.objects.all()
    return render(request, 'certificates.html', {'certificates': certificates})