from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm

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

    context = {'customer': customer , 'orders': orders , 'total_order': total_order}

    return render(request, 'accounts/customers.html', context)

#tạo form thêm mới order
def create_order(request):
    form = OrderForm()
    context ={'form':form}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
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