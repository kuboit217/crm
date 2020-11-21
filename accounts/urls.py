from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('products/', views.products, name='product'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('users/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account'),


    path('customers/<str:pk>/', views.customers , name='customer'),
    
    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),
]
