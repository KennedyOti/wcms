from django.http import HttpResponse
from django.shortcuts import redirect

# Authentication Decorator
def unauthenticated_user(view_func):
    def wrapper_func(request, *argd, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
             return view_func(request, *argd, **kwargs)
    return wrapper_func

# Roles Decorator
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *argd, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *argd, **kwargs)
            else:
                return HttpResponse('You are not authorised to access this page')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'member':
            return redirect('profile', pk=request.user.pk)
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_function
