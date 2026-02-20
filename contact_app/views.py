from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import ContactMessage

@login_required(login_url='accounts:login')
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save to database
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )
        
        # Send email to admin
        admin_subject = f"New Contact Form Message from {name}"
        admin_message = f"""
        New message from your portfolio website:
        
        Name: {name}
        Email: {email}
        Message: {message}
        
        This message was sent on {contact.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        try:
            # Send to admin
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            print(f"Email sent to admin: {settings.CONTACT_EMAIL}")  # Debug
            
            # Send confirmation to user
            user_subject = "Thank you for contacting Srujitha Jasmine!"
            user_message = f"""
            Dear {name},
            
            Thank you for reaching out to me through my portfolio website. I have received your message and will get back to you as soon as possible.
            
            Your message: {message}
            
            Best regards,
            Srujitha Jasmine Baggam
            AI ML Engineer
            """
            
            send_mail(
                user_subject,
                user_message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            print(f"Confirmation email sent to user: {email}")  # Debug
            
            messages.success(request, "Message sent successfully! Check your email for confirmation.")
            
        except Exception as e:
            print(f"Email error: {str(e)}")  # Debug
            messages.warning(request, "Message saved but email could not be sent. I'll still get back to you soon!")
        
        return redirect('contact:success')
    
    return render(request, 'contact.html')

@login_required(login_url='accounts:login')
def contact_success(request):
    return render(request, 'contact_success.html')