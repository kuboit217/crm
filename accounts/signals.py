from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from .models import Customer

def customer_profile(sender,instance, created , **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group) #tự thêm group vào user
        #gắn user vào tên khách hàng
        Customer.objects.create(user=instance,name=instance.username,)


post_save.connect(customer_profile, sender= User)