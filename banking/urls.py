from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from .views import home, vc, about_us, new_cus, trans, transhistory, welcome

urlpatterns = [
    path('', welcome),
    path('home/', home, name='home'),
    path('view_customer/', vc, name='view_customer'),
    path('about_us/', about_us, name='about_us'),
    path('new_customer/', new_cus, name='new_cus'),
    path('transfer_money/', trans, name='trans'),
    path('trans_history/', transhistory, name='transhistory')

]
