from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from projects_app.models import Project, Certificate
from contact_app.models import ContactMessage
from accounts_app.models import Profile
from django.core.paginator import Paginator
from django.utils import timezone

# ===== AUTHORIZED USERS LIST =====
AUTHORIZED_USERS = ['sruji', 'admin', 'jasmine', 'srujitha']
AUTHORIZED_EMAILS = ['srujithajasmineb@gmail.com', 'baggamsrujithajasmine@gmail.com']

# ===== PUBLIC HOME PAGE - NO LOGIN REQUIRED =====
def home_view(request):
    """Public home page - shows projects and certificates"""
    projects = Project.objects.all().order_by('-created_date')[:6]  # Latest 6 projects
    certificates = Certificate.objects.all().order_by('-issued_date')[:4]  # Latest 4 certificates
    
    context = {
        'projects': projects,
        'certificates': certificates,
    }
    return render(request, 'home.html', context)

# ===== AUTHENTICATION VIEWS =====
def signup_view(request):
    """Signup is completely disabled - redirects to home"""
    messages.error(request, '❌ Sign up is disabled. Only administrator can access.')
    return redirect('home')

def login_view(request):
    """User login for portfolio access - only for authorized users"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if username in AUTHORIZED_USERS or user.email in AUTHORIZED_EMAILS:
                    login(request, user)
                    messages.success(request, f'✨ Welcome back, {username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, '⛔ You are not authorized to access this portfolio.')
                    return redirect('home')
            else:
                messages.error(request, '❌ Invalid username or password.')
        else:
            messages.error(request, '❌ Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Logout user and redirect to home"""
    logout(request)
    messages.success(request, '👋 You have been logged out successfully.')
    return redirect('home')

def admin_portal_login(request):
    """Separate admin portal login - only for staff"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            # Only staff and authorized users can access admin portal
            if user is not None and user.is_staff:
                if username in AUTHORIZED_USERS or user.email in AUTHORIZED_EMAILS:
                    login(request, user)
                    messages.success(request, f'🚀 Welcome to Admin Portal, {username}!')
                    return redirect('admin:index')
                else:
                    messages.error(request, '⛔ You are not authorized for admin access.')
            else:
                messages.error(request, '❌ Invalid admin credentials.')
        else:
            messages.error(request, '❌ Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'admin/admin_login.html', {'form': form})

# ===== PROTECTED DASHBOARD (Login Required) =====
@login_required(login_url='login')
def dashboard(request):
    """User dashboard - only for authorized users"""
    # Check if user is authorized
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('home')
    
    # Get counts for dashboard stats
    total_projects = Project.objects.count()
    total_certificates = Certificate.objects.count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_users = User.objects.count()
    
    # Get recent items
    recent_projects = Project.objects.all().order_by('-created_date')[:5]
    recent_certificates = Certificate.objects.all().order_by('-issued_date')[:5]
    recent_messages = ContactMessage.objects.all().order_by('-timestamp')[:5]
    
    # Get user profile
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'total_projects': total_projects,
        'total_certificates': total_certificates,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'total_users': total_users,
        'recent_projects': recent_projects,
        'recent_certificates': recent_certificates,
        'recent_messages': recent_messages,
        'profile': profile,
        'user': request.user,
        'today': timezone.now(),
    }
    return render(request, 'dashboard.html', context)

# ===== PROJECT MANAGEMENT VIEWS (STAFF ONLY) =====
@staff_member_required(login_url='admin_portal_login')
def manage_projects(request):
    """Manage all projects - staff only"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    projects_list = Project.objects.all().order_by('-created_date')
    paginator = Paginator(projects_list, 10)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'manage_projects.html', {'projects': projects})

@staff_member_required(login_url='admin_portal_login')
def project_create(request):
    """Create a new project"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
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
        messages.success(request, f'✅ Project "{title}" created successfully!')
        return redirect('accounts:manage_projects')
    
    return render(request, 'project_form.html')

@staff_member_required(login_url='admin_portal_login')
def project_edit(request, pk):
    """Edit an existing project"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.tech_stack = request.POST.get('tech_stack')
        project.github_link = request.POST.get('github_link')
        project.live_demo_link = request.POST.get('live_demo_link')
        
        if request.FILES.get('image'):
            project.image = request.FILES.get('image')
        
        project.save()
        messages.success(request, f'✅ Project "{project.title}" updated successfully!')
        return redirect('accounts:manage_projects')
    
    return render(request, 'project_form.html', {'project': project})

@staff_member_required(login_url='admin_portal_login')
def project_delete(request, pk):
    """Delete a project"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'✅ Project "{title}" deleted successfully!')
        return redirect('accounts:manage_projects')
    
    return render(request, 'confirm_delete_project.html', {'project': project})

# ===== CERTIFICATE MANAGEMENT VIEWS (STAFF ONLY) =====
@staff_member_required(login_url='admin_portal_login')
def manage_certificates(request):
    """Manage all certificates - staff only"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    certificates_list = Certificate.objects.all().order_by('-issued_date')
    paginator = Paginator(certificates_list, 10)
    page = request.GET.get('page')
    certificates = paginator.get_page(page)
    return render(request, 'manage_certificates.html', {'certificates': certificates})

@staff_member_required(login_url='admin_portal_login')
def certificate_create(request):
    """Create a new certificate"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
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
        messages.success(request, f'✅ Certificate "{title}" created successfully!')
        return redirect('accounts:manage_certificates')
    
    return render(request, 'certificate_form.html')

@staff_member_required(login_url='admin_portal_login')
def certificate_edit(request, pk):
    """Edit an existing certificate"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
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
        messages.success(request, f'✅ Certificate "{certificate.title}" updated successfully!')
        return redirect('accounts:manage_certificates')
    
    return render(request, 'certificate_form.html', {'certificate': certificate})

@staff_member_required(login_url='admin_portal_login')
def certificate_delete(request, pk):
    """Delete a certificate"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    certificate = get_object_or_404(Certificate, pk=pk)
    
    if request.method == 'POST':
        title = certificate.title
        certificate.delete()
        messages.success(request, f'✅ Certificate "{title}" deleted successfully!')
        return redirect('accounts:manage_certificates')
    
    return render(request, 'confirm_delete_certificate.html', {'certificate': certificate})

# ===== MESSAGE MANAGEMENT VIEWS (STAFF ONLY) =====
@staff_member_required(login_url='admin_portal_login')
def manage_messages(request):
    """Manage all contact messages - staff only"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    messages_list = ContactMessage.objects.all().order_by('-timestamp')
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    messages_list = paginator.get_page(page)
    return render(request, 'manage_messages.html', {'messages': messages_list})

@staff_member_required(login_url='admin_portal_login')
def mark_message_read(request, pk):
    """Mark a message as read"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    messages.success(request, f'✅ Message from {message.name} marked as read.')
    return redirect('accounts:manage_messages')

@staff_member_required(login_url='admin_portal_login')
def delete_message(request, pk):
    """Delete a message"""
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, '⛔ Unauthorized access.')
        return redirect('admin_portal_login')
    
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        name = message.name
        message.delete()
        messages.success(request, f'✅ Message from {name} deleted successfully.')
        return redirect('accounts:manage_messages')
    return render(request, 'confirm_delete_message.html', {'message': message})