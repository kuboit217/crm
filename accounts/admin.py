from django.contrib import admin
# Register your models here.

from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','phone','email','date_created']
    list_filter = ['date_created']
    search_fields = ['name']

admin.site.register(Customer, CustomerAdmin)

admin.site.register(Product)

admin.site.register(Order)
