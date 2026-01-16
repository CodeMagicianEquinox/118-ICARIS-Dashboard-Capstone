# Create this file: grc_dashboard/decorators.py

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def poam_permission_required(view_func):
    """
    Decorator to check if user has permission to manage PO&AMs.
    Only admins and Security department users can manage PO&AMs.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Admin/staff users always have permission
        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        
        # Check if user has profile and is in Security department
        if hasattr(request.user, 'profile'):
            if request.user.profile.department and request.user.profile.department.name == 'Security':
                return view_func(request, *args, **kwargs)
        
        # User doesn't have permission
        messages.error(request, 'You do not have permission to manage PO&AMs. Only Security department users and administrators can add or modify PO&AMs.')
        return redirect('issue_tracking')
    
    return wrapper