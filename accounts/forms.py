from django.forms import ModelForm
from .models import Order

#tạo form tạo mới order
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'