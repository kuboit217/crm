from django.contrib import admin
# Register your models here.

from .models import *
#chỉnh lại hiển thị Custemer
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','phone','email','date_created']
    list_filter = ['date_created']
    search_fields = ['name']

#chỉnh lại hiển thị Order    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['custumer','product','status']
    list_filter = ['date_created']
    search_fields = ['custumer']

#chỉnh lại hiển thị product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category']
    list_filter = ['date_created']
    search_fields = ['name']

#đăng ký hiện lên admin    
admin.site.register(Customer, CustomerAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(Tag)
