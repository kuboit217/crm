from django.http import HttpResponse
from django.shortcuts import redirect

#chuyển hướng user đăng nhập khi nào register and login thì chuyển sang home
def unauthenticated_user(view_func):
    def wapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wapper_func

#kiểm tra role đăng nhập
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wapper_func(request, *args, **kwargs):
            group = None
            #kiểm tra sự tồn tại của group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to access this page')
        return wapper_func
    return decorator


#admin only
def andmin_only(view_func):
    def wapper_func(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer': 
            return redirect('user-page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wapper_func
