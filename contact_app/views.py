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
        
        print(f"\n{'='*50}")
        print(f"📝 Contact form submission:")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Message: {message[:50]}...")
        
        # Save to database
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )
        print(f"💾 Saved to database (ID: {contact.id})")
        print(f"📅 Timestamp: {contact.timestamp}")
        
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
            # Check if CONTACT_EMAIL is set
            print(f"📧 EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            print(f"📧 CONTACT_EMAIL: {getattr(settings, 'CONTACT_EMAIL', 'NOT SET')}")
            
            # Send to admin
            print("📧 Sending admin email...")
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            print(f"✅ Admin email sent to: {settings.CONTACT_EMAIL}")
            
            # Send confirmation to user
            print(f"📧 Sending confirmation email to user: {email}...")
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
            print(f"✅ Confirmation email sent to: {email}")
            
            messages.success(request, "Message sent successfully! Check your email for confirmation.")
            
        except Exception as e:
            print(f"❌ EMAIL ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.warning(request, f"Message saved but email could not be sent. Error: {str(e)}")
        
        print(f"{'='*50}\n")
        return redirect('contact:success')
    
    return render(request, 'contact.html')

# ===== ADD THIS MISSING FUNCTION =====
@login_required(login_url='accounts:login')
def contact_success(request):
    """
    Contact form success page
    """
    print("✅ Contact success page accessed")
    return render(request, 'contact_success.html')