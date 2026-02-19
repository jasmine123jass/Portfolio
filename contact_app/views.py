from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import ContactMessage

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
        
        try:
            # Send email to admin
            admin_subject = f"New Contact from {name}"
            admin_message = render_to_string('emails/admin_notification.html', {
                'name': name,
                'email': email,
                'message': message
            })
            
            admin_email = EmailMessage(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL]
            )
            admin_email.content_subtype = "html"
            admin_email.send()
            
            # Send confirmation to user
            user_subject = "Thank you for contacting me!"
            user_message = render_to_string('emails/user_confirmation.html', {
                'name': name
            })
            
            user_email = EmailMessage(
                user_subject,
                user_message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            user_email.content_subtype = "html"
            user_email.send()
            
            messages.success(request, "Message sent successfully! Check your email for confirmation.")
        except Exception as e:
            messages.warning(request, "Message saved but email notification could not be sent.")
        
        return redirect('contact:success')
    
    return render(request, 'contact.html')

def contact_success(request):
    return render(request, 'contact_success.html')