from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
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

# ===== ONLY YOU CAN LOGIN =====
# Add your username and email here - ONLY THESE WILL WORK
AUTHORIZED_USERS = ['srujitha', 'admin', 'jasmine']  # Add your usernames
AUTHORIZED_EMAILS = ['srujithajasmineb@gmail.com']  # Add your email

def signup_view(request):
    # COMPLETELY DISABLE SIGNUP - No one can create account
    messages.error(request, 'Sign up is disabled. Only the administrator can access this portfolio.')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            # Check if user exists and is authorized (ONLY YOU)
            if user is not None:
                # Allow only specific users (YOU)
                if username in AUTHORIZED_USERS or user.email in AUTHORIZED_EMAILS:
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('home')
                else:
                    # Unauthorized user - show error and logout any existing session
                    messages.error(request, 'You are not authorized to access this portfolio.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            # Check if user is authorized admin (ONLY YOU)
            if user is not None and user.is_staff:
                # Double-check it's you
                if username in AUTHORIZED_USERS or user.email in AUTHORIZED_EMAILS:
                    login(request, user)
                    messages.success(request, f'Welcome Admin, {username}!')
                    return redirect('admin:index')
                else:
                    messages.error(request, 'You are not authorized for admin access.')
            else:
                messages.error(request, 'Invalid admin credentials.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'admin/login.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    # Get counts for dashboard stats
    total_projects = Project.objects.count()
    total_certificates = Certificate.objects.count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # Get recent items (last 5)
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
        'recent_projects': recent_projects,
        'recent_certificates': recent_certificates,
        'recent_messages': recent_messages,
        'profile': profile,
        'user': request.user,
        'today': timezone.now(),
    }
    return render(request, 'dashboard.html', context)

@staff_member_required(login_url='admin_login')
def admin_dashboard(request):
    # Check if user is authorized admin (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized admin access.')
        return redirect('admin_login')
    
    # Get all stats
    total_projects = Project.objects.count()
    total_certificates = Certificate.objects.count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_users = User.objects.count()
    
    # Get recent items
    recent_projects = Project.objects.all().order_by('-created_date')[:5]
    recent_certificates = Certificate.objects.all().order_by('-issued_date')[:5]
    recent_messages = ContactMessage.objects.all().order_by('-timestamp')[:5]
    
    # Combine and sort recent actions
    recent_actions = []
    
    for project in recent_projects:
        recent_actions.append({
            'type': 'project',
            'name': project.title,
            'date': project.created_date,
            'icon': 'fa-project-diagram',
            'color': '#003366'
        })
    
    for cert in recent_certificates:
        recent_actions.append({
            'type': 'certificate',
            'name': f"{cert.title} - {cert.issuer}",
            'date': cert.issued_date,
            'icon': 'fa-certificate',
            'color': '#1e4a7a'
        })
    
    for msg in recent_messages:
        recent_actions.append({
            'type': 'message',
            'name': f"{msg.name} - {msg.email}",
            'date': msg.timestamp,
            'icon': 'fa-envelope',
            'color': '#ff6b6b'
        })
    
    # Sort by date (newest first)
    recent_actions.sort(key=lambda x: x['date'], reverse=True)
    recent_actions = recent_actions[:10]
    
    context = {
        'total_projects': total_projects,
        'total_certificates': total_certificates,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'total_users': total_users,
        'recent_actions': recent_actions,
        'recent_projects': recent_projects,
        'recent_certificates': recent_certificates,
        'recent_messages': recent_messages,
        'user': request.user,
        'today': timezone.now(),
    }
    return render(request, 'admin_dashboard.html', context)

# ===== STAFF ONLY VIEWS (But only YOU are staff) =====
@staff_member_required(login_url='admin_login')
def manage_projects(request):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    projects_list = Project.objects.all().order_by('-created_date')
    paginator = Paginator(projects_list, 10)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'manage_projects.html', {'projects': projects})

@staff_member_required(login_url='admin_login')
def manage_certificates(request):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    certificates_list = Certificate.objects.all().order_by('-issued_date')
    paginator = Paginator(certificates_list, 10)
    page = request.GET.get('page')
    certificates = paginator.get_page(page)
    return render(request, 'manage_certificates.html', {'certificates': certificates})

@staff_member_required(login_url='admin_login')
def manage_messages(request):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    messages_list = ContactMessage.objects.all().order_by('-timestamp')
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    messages_list = paginator.get_page(page)
    return render(request, 'manage_messages.html', {'messages': messages_list})

@staff_member_required(login_url='admin_login')
def mark_message_read(request, pk):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    messages.success(request, f'Message from {message.name} marked as read.')
    return redirect('accounts:manage_messages')

@staff_member_required(login_url='admin_login')
def delete_message(request, pk):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        name = message.name
        message.delete()
        messages.success(request, f'Message from {name} deleted successfully.')
        return redirect('accounts:manage_messages')
    return render(request, 'confirm_delete_message.html', {'message': message})

@staff_member_required(login_url='admin_login')
def project_create(request):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
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
        return redirect('accounts:manage_projects')
    
    return render(request, 'project_form.html')

@staff_member_required(login_url='admin_login')
def project_edit(request, pk):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
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
        messages.success(request, f'Project "{project.title}" updated successfully!')
        return redirect('accounts:manage_projects')
    
    return render(request, 'project_form.html', {'project': project})

@staff_member_required(login_url='admin_login')
def project_delete(request, pk):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted successfully!')
        return redirect('accounts:manage_projects')
    
    return render(request, 'confirm_delete_project.html', {'project': project})

@staff_member_required(login_url='admin_login')
def certificate_create(request):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
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
        return redirect('accounts:manage_certificates')
    
    return render(request, 'certificate_form.html')

@staff_member_required(login_url='admin_login')
def certificate_edit(request, pk):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
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
        return redirect('accounts:manage_certificates')
    
    return render(request, 'certificate_form.html', {'certificate': certificate})

@staff_member_required(login_url='admin_login')
def certificate_delete(request, pk):
    # Check if user is authorized (ONLY YOU)
    if request.user.username not in AUTHORIZED_USERS and request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, 'Unauthorized access.')
        return redirect('admin_login')
    
    certificate = get_object_or_404(Certificate, pk=pk)
    
    if request.method == 'POST':
        title = certificate.title
        certificate.delete()
        messages.success(request, f'Certificate "{title}" deleted successfully!')
        return redirect('accounts:manage_certificates')
    
    return render(request, 'confirm_delete_certificate.html', {'certificate': certificate})