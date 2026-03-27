from django.shortcuts import redirect
from django.contrib import messages

# Blocks access to admin-only views
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__wrapped__ = view_func
    return wrapper

# Blocks access to pages that require login
def login_required_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__wrapped__ = view_func
    return wrapper