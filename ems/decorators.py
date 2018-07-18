from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('employee_list'))
        return wrap
    return decorator

def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.role == "HR":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_list'))
    return wrap
