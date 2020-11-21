from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm , CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout

# Create your views here.
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
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

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
def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context ={'item':order}
    return render(request, 'accounts/delete_order.html', context)

#tạo login
def loginPage(request):
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
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Accout was create for '+ user)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

#tạo phần logout
def logoutUser(request):
    logout(request)
    return redirect('login')