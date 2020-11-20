import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['custumer','date_created']