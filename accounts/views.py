from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.models import Group

#view của bạn
from .models import *
from .forms import OrderForm , CreateUserForm
from .filters import OrderFilter
#đưa decorators vào để kiểm tra đăng nhập
from .decorators import unauthenticated_user, allowed_users , andmin_only

# Create your views here.
@login_required(login_url='login')
@andmin_only
def home(request):
    customers = Customer.objects.all().order_by('-date_created')
    orders = Order.objects.all().order_by('-date_created')

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers': customers, 'orders': orders, 'total_orders': total_orders,
        'delivered':delivered , 'pending':pending
    }
    return render(request, 'accounts/dashboard.html', context)
#lấy danh sách sản phẩm
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

#tạo phần khách hàng    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()

    #tạo tìm kiếm trong customer
    customer_filter = OrderFilter(request.GET, queryset= orders)
    orders = customer_filter.qs

    context = {'customer': customer , 'orders': orders , 'total_order': total_order, 'customer_filter': customer_filter}

    return render(request, 'accounts/customers.html', context)

#tạo form thêm mới order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer,Order , fields = ('product','status'), extra =5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer': customer})  
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context ={'formset':formset}
    return render(request, 'accounts/order_form.html', context)

#tọ form update order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form': form}
    return render(request, 'accounts/order_form.html', context)

#tạo xóa order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context ={'item':order}
    return render(request, 'accounts/delete_order.html', context)

#tạo login
@unauthenticated_user
def loginPage(request):
    #nếu chưa đăng nhập thì mới có đến login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is correct')

    context = {}
    return render(request, 'accounts/login.html', context)

#tạo form đăng ký
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group) #tự thêm group vào user
            #gắn user vào tên khách hàng
            Customer.objects.create(user=user,name=user.username,)
            messages.success(request,'Accout was create for '+ username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

#tạo phần logout
def logoutUser(request):
    logout(request)
    return redirect('login')

#tạo trang vào user
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders': orders, 'total_orders': total_orders,
        'delivered':delivered , 'pending':pending}
    return render(request, 'accounts/users.html', context)