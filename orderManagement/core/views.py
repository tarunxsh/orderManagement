from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
import logging
import time
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Order
from .task import AssignDboy,pickupOrder
from .logs import log1,log2



# helper function
def get_Object_Or_None(model , *args,**kwargs):
	try:
		return model.objects.get(*args,**kwargs)
	except model.DoesNotExist:
		return None

# ====================================================================
# ViewsS Starts
# WEBHOOK TO PLACE NEW ORDER
@csrf_exempt
@require_POST 
def neworder(request):
	print("Order Received")
	username = request.POST.get("username")
	lattitude = request.POST.get("lattitude")
	longitude = request.POST.get("longitude")
	amt = request.POST.get("amt")

	newOrder = Order.objects.create(owner=username, lattitude=lattitude,longitude=longitude,order_st='RCD',amt=amt)
	orderID = newOrder.order_id

	# logging msg
	log1(orderID=orderID,owner=username,lattitude=lattitude,longitude=longitude,order_st="order_received")	
	
	# celery shared task
	AssignDboy.delay(orderID)
	pickupOrder.delay(orderID)
	return HttpResponse("Received")



# WEBHOOK TO RECEIVE ORDER BY OWNER
@csrf_exempt
@require_POST 
def delivered(request):
	# delivery data recvd
	username = request.POST.get("username")
	lattitude = request.POST.get("lattitude")
	longitude = request.POST.get("longitude")
	amt = request.POST.get("amt")

	currentOrder = get_Object_Or_None(Order,owner=username,lattitude=lattitude,longitude=longitude,order_st='PKD',amt=amt)
	if(currentOrder == None):
		print("Already delivered")
		print("Thank You")
		return HttpResponse("Already Delivered")

	orderID = currentOrder.order_id
	currentOrder.order_st = 'DLD'
	Dboy = currentOrder.dboy_name 
	Dboy.earnings += float(amt)
	Dboy.status = 'FRE'
	Dboy.save()
	currentOrder.payment_st = True
	currentOrder.save()
	
	# logging status
	log1(orderID,username,lattitude,longitude,Dboy.name,amt,"order_delivered",currentOrder.timeTaken)
	print("order-{} delivered".format(orderID))
	print("Thank You")
	return HttpResponse("Delivered")





