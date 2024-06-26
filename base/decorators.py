from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, HttpResponseRedirect

def group_required(group_name, permitted_group_mappings=None):


    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.groups.filter(name=group_name).exists():
               
                if permitted_group_mappings:
                    for group in user.groups.all():
                        if group.name in permitted_group_mappings:
                            return redirect(permitted_group_mappings[group.name])
          
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


from django.urls import reverse

def prevent_logged_in_users(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect back to previous page if HTTP_REFERER is available
            redirect_to = request.META.get('HTTP_REFERER')
            return redirect(redirect_to)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper