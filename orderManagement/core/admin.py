from django.contrib import admin
from .models import Order , Dboy
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("order_id" , "owner" , "order_st","dboy_name","payment_st","amt")



@admin.register(Dboy)
class DboyAdmin(admin.ModelAdmin):
	list_display = ("name","status","earnings")
