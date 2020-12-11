from django.db import models

# Custom Model Manager to get list of  available delivery boys only
class getAvailaibleDboys(models.Manager):
	def get_queryset(self):
		return super(getAvailaibleDboys,self).get_queryset().filter(status='FRE')



# Delivery Boy Database Model
class Dboy(models.Model):

	STATUS = (
		('ASD','assigned'),
		('FRE','free'),
	)

	name = models.CharField(max_length=20,db_column="name")
	status = models.CharField(max_length=5,choices=STATUS,default='FRE',db_column="dboy_st")
	kms =  models.FloatField(default=0.0,db_column="kms")
	dailyDrivingTime = models.FloatField(default=0.0,db_column="dailyDrivingTime")
	totalOrderHandled = models.IntegerField(default=0,db_column="totalOrderHandled")
	earnings = models.FloatField(default=0.0,db_column="earnings")

	objects = models.Manager()
	free = getAvailaibleDboys()

	def __str__(self):
		return "{}:{}".format(self.name,self.status)



# Order Database Model
class Order(models.Model):

	STATUS = (
		('RCD','rcvd'),
		('ASD','dboy_asngd'),
		('PKD','odr_pkd'),
		('DLD','dlvrd'),
	)

	order_id = models.AutoField(primary_key=True,db_column="order_id")
	owner    = models.CharField(max_length=20,db_column="owner")
	lattitude = models.FloatField(db_column="lattitude")
	longitude = models.FloatField(db_column="longitude")
	created_at = models.DateTimeField(auto_now_add=True,db_column="created_at")
	order_st = models.CharField(max_length=5,choices=STATUS,db_column="order_st")
	dboy_name = models.ForeignKey(Dboy,on_delete=models.SET_NULL,blank=True,null=True,related_name="dboy")
	updated = models.DateTimeField(auto_now=True,db_column="updated")	#not shown in admin / auto update
	timeTaken = models.IntegerField(default=0,db_column="timeTaken")	#time in minutes only
	payment_st = models.BooleanField(default=False, db_column="payment_st")
	amt = models.FloatField(default=0.0,db_column="amt")



	def isAssigned(self):
		return self.order_st=='ASD'
	

	def __str__(self):
		return "{}.{}".format(self.order_id,self.owner)



