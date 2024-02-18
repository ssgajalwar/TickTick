from functools import wraps
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            group_names = request.user.groups.values_list('name', flat=True)

            if any(role in group_names for role in allowed_roles):
                return view_func(request, *args, **kwargs)
            else:
                print("unauthorized user")
                return redirect('/demoapp/hello/')  # Redirect to an unauthorized access page

        return wrapper
    return decorator
