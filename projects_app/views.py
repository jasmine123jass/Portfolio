from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Project, Certificate
from accounts_app.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

# ===== PUBLIC VIEWS - No login required =====

def home(request):
    """Home page - PUBLIC"""
    projects = Project.objects.all()[:3]  # Only show 3 projects on home
    certificates = Certificate.objects.all()[:3]  # Only show 3 certificates on home
    profile = Profile.objects.first()
    
    context = {
        'projects': projects,
        'certificates': certificates,
        'profile': profile,
    }
    return render(request, 'home.html', context)

def project_list(request):
    """Project list page - PUBLIC"""
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def project_detail(request, slug):
    """Project detail page - PUBLIC"""
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_detail.html', {'project': project})

def certificate_list(request):
    """Certificate list page - PUBLIC"""
    certificates = Certificate.objects.all()
    return render(request, 'certificates.html', {'certificates': certificates})

# ===== ADMIN ONLY VIEWS - Require staff login =====

@staff_member_required(login_url='admin:login')
def project_create(request):
    """Create a new project - ADMIN ONLY"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tech_stack = request.POST.get('tech_stack')
        github_link = request.POST.get('github_link')
        live_demo_link = request.POST.get('live_demo_link')
        image = request.FILES.get('image')
        
        project = Project.objects.create(
            title=title,
            description=description,
            tech_stack=tech_stack,
            github_link=github_link,
            live_demo_link=live_demo_link,
            image=image
        )
        messages.success(request, f'Project "{title}" created successfully!')
        return redirect('projects:project_detail', slug=project.slug)
    
    return render(request, 'project_form.html')

@staff_member_required(login_url='admin:login')
def project_update(request, slug):
    """Update an existing project - ADMIN ONLY"""
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.tech_stack = request.POST.get('tech_stack')
        project.github_link = request.POST.get('github_link')
        project.live_demo_link = request.POST.get('live_demo_link')
        
        if request.FILES.get('image'):
            project.image = request.FILES.get('image')
        
        project.save()
        messages.success(request, f'Project "{project.title}" updated successfully!')
        return redirect('projects:project_detail', slug=project.slug)
    
    return render(request, 'project_form.html', {'project': project})

@staff_member_required(login_url='admin:login')
def project_delete(request, slug):
    """Delete a project - ADMIN ONLY"""
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted successfully!')
        return redirect('projects:project_list')
    
    return render(request, 'confirm_delete.html', {'project': project})

@staff_member_required(login_url='admin:login')
def certificate_create(request):
    """Create a new certificate - ADMIN ONLY"""
    if request.method == 'POST':
        title = request.POST.get('title')
        issuer = request.POST.get('issuer')
        issued_date = request.POST.get('issued_date')
        credential_id = request.POST.get('credential_id')
        credential_url = request.POST.get('credential_url')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        certificate = Certificate.objects.create(
            title=title,
            issuer=issuer,
            issued_date=issued_date,
            credential_id=credential_id,
            credential_url=credential_url,
            description=description,
            image=image
        )
        messages.success(request, f'Certificate "{title}" created successfully!')
        return redirect('certificate_list')
    
    return render(request, 'certificate_form.html')

@staff_member_required(login_url='admin:login')
def certificate_update(request, pk):
    """Update an existing certificate - ADMIN ONLY"""
    certificate = get_object_or_404(Certificate, pk=pk)
    
    if request.method == 'POST':
        certificate.title = request.POST.get('title')
        certificate.issuer = request.POST.get('issuer')
        certificate.issued_date = request.POST.get('issued_date')
        certificate.credential_id = request.POST.get('credential_id')
        certificate.credential_url = request.POST.get('credential_url')
        certificate.description = request.POST.get('description')
        
        if request.FILES.get('image'):
            certificate.image = request.FILES.get('image')
        
        certificate.save()
        messages.success(request, f'Certificate "{certificate.title}" updated successfully!')
        return redirect('certificate_list')
    
    return render(request, 'certificate_form.html', {'certificate': certificate})

@staff_member_required(login_url='admin:login')
def certificate_delete(request, pk):
    """Delete a certificate - ADMIN ONLY"""
    certificate = get_object_or_404(Certificate, pk=pk)
    
    if request.method == 'POST':
        title = certificate.title
        certificate.delete()
        messages.success(request, f'Certificate "{title}" deleted successfully!')
        return redirect('certificate_list')
    
    return render(request, 'confirm_delete_certificate.html', {'certificate': certificate})