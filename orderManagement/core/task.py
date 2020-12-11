import math
import sys
import time
from django.utils import timezone
from datetime import datetime,timedelta
from celery import shared_task
from haversine import haversine, Unit

from .models import Order ,Dboy
from .logs import log1,log2,second_logger


@shared_task
def AssignDboy(orderID):
	boysAvailable = Dboy.free.all()
	while(not boysAvailable):
		time.sleep(5)
		print("all busy")
		boysAvailable = Dboy.free.all()

	# deleivery boy available
	dboy = boysAvailable[0]

	# order data
	currentOrder = Order.objects.get(order_id=orderID)
	username = currentOrder.owner
	lattitude = currentOrder.lattitude
	longitude = currentOrder.longitude
	orderLocation = (lattitude,longitude)
	
	
	currentOrder.dboy_name = dboy

	# unpack returned tuple
	nearestBranchName,nearestBranchLocation,nearestBranchDistance = nearestRestaurant(orderLocation)

	nearestBranchDistanceFromDboy = haversine((28.6037837,77.0569728),nearestBranchLocation)
	
	# total km travelled by deleivery boy
	kmsTravelled = nearestBranchDistanceFromDboy + nearestBranchDistance
	# print(kmsTravelled)
	dboy.kms += kmsTravelled
	dboy.dailyDrivingTime += kmsTravelled	#reset everyday
	
	# According to problem statement time to complete order is equal to total distances
	currentOrder.timeTaken = math.ceil(kmsTravelled)   #handling case with 0.7 km using ceil

	dboy.status = 'ASD'
	dboy.totalOrderHandled += 1
	currentOrder.order_st  = 'ASD'

	# logging status
	log1(orderID,username,lattitude,longitude,dboy.name,order_st="delivery_boy_assigned")
	print("{} assigned".format(dboy.name))
	
	currentOrder.save() 
	dboy.save()
	return "assigned"



@shared_task
def pickupOrder(orderID):
	# order data
	currentOrder = Order.objects.get(order_id=orderID)
	username = currentOrder.owner
	lattitude = currentOrder.lattitude
	longitude = currentOrder.longitude

	while(not currentOrder.isAssigned()):
		time.sleep(10)
		print("order-{} not assigned".format(orderID))
		currentOrder = Order.objects.get(order_id=orderID)

	timeTaken = currentOrder.timeTaken
	currentOrder.order_st = 'PKD'
	currentOrder.save()

	# logging status
	log1(orderID,username,lattitude,longitude,currentOrder.dboy_name.name,order_st="order_picked")
	print("order-{} pkd".format(orderID))
	print("order-{}-TimeTaken-{}".format(orderID,timeTaken))
	
	# scheduling deleivery
	scheduledTime = timezone.localtime(timezone.now())+timedelta(minutes=timeTaken)
	print("scheduledTime:{}".format(scheduledTime))
	print("delivering order-{}".format(orderID))
	delivery.apply_async((orderID,timeTaken),eta=scheduledTime)
	return "pkd"

# schedule delivery
@shared_task
def delivery(orderID,timeTaken):
	
	# order data
	currentOrder = Order.objects.get(order_id=orderID)

	# if order is already received from simulator web page
	if(currentOrder.order_st=='DLD'):
		print("Already delivered")
		print("Thank You")
		return "Already delivered"

	# if not received already then deliver automatically on scheduled time
	username = currentOrder.owner
	lattitude = currentOrder.lattitude
	longitude = currentOrder.longitude
	orderID = currentOrder.order_id
	currentOrder.order_st = 'DLD'
	Dboy = currentOrder.dboy_name 
	Dboy.earnings += currentOrder.amt
	Dboy.status = 'FRE'
	Dboy.save()
	currentOrder.payment_st = True
	currentOrder.save()
	
	# logging status
	log1(orderID,username,lattitude,longitude,Dboy.name,currentOrder.amt,"order_delivered",timeTaken)
	print("order-{} delivered".format(orderID))
	print("Thank You")
	return "delivery complete"



# ========================================================================
# Helper Function
# calculate Nearest Restaurant Based on Order Location
def nearestRestaurant(orderLocation):
	BranchCoordinates = {
		"Amartya" : (28.6037837,77.0569728),
		"Swalini" : (28.5921784,77.0598052),
		"Rituraj" : (28.5904073,77.0558999),
		"Prabhutva" : (28.5885043,77.0592473),
		"Sanjeevini" : (28.5882877,77.0546661),
	}

	# default
	nearestBranchName = "Amartya"
	nearestBranchLocation = (28.6037837,77.0569728)
	nearestBranchDistance =  sys.maxsize

	# calculating and comparing distances
	for branch,loc in BranchCoordinates.items():
		currentBranchDistance = haversine(orderLocation,loc)
		if(currentBranchDistance < nearestBranchDistance):
			nearestBranchDistance = currentBranchDistance
			nearestBranchName = branch
			nearestBranchLocation = loc

	print("\nBranch : {}\nLocation : {}\nDistance : {}\n".format(
		nearestBranchName, nearestBranchLocation ,nearestBranchDistance))

	return (nearestBranchName,nearestBranchLocation,nearestBranchDistance)



# ======================================================
# log all delivery boy detail everyday
@shared_task
def logDboyDetails():
	# second_logger.info("============================================================")
	# second_logger.info(datetime.now())
	# second_logger.info("============================================================")
	Dboys = Dboy.objects.all()
	for dboy in Dboys:
		name = dboy.name
		kms = dboy.kms
		earnings = dboy.earnings
		totalOrderHandled = dboy.totalOrderHandled
		dailyDrivingTime = dboy.dailyDrivingTime
		log2(name,kms,earnings,totalOrderHandled,dailyDrivingTime)

		# reset daily driving time
		dailyDrivingTime = 0
		dboy.save()

	return "all dboys detail logged"



# RUN CMD
# celery -A orderManagement worker --concurrency=1 --loglevel=info