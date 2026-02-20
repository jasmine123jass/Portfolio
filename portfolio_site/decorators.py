from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def public_view_allowed(view_func):
    """Decorator for views that should be public (login page, etc.)"""
    return view_func

def login_required_message(view_func):
    """Decorator that requires login and shows message"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to view the portfolio.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper