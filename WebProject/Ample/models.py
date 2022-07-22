from django.db import models
from django.contrib.auth.models import User
# Create your models here.

CATEGORY_CHOICES = (
  ('Admin','ADMIN'),
  ('Customer','CUSTOMER'),
  ('Driver','DRIVER'),
  ('Guest','GUEST'),
)

class UserProfile(models.Model):
    UserID  = models.ForeignKey(User, on_delete=models.CASCADE)
    Image   = models.ImageField(upload_to='images/',default='images/default.png')
    UserType= models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    Address = models.CharField(max_length=150)
    Time    = models.DateTimeField(auto_now=True)
    def __str__(self):
      return str(self.id)


DELIVERY_CHOICES = (
  ('Delivery with Cooler','DELIVERY WITH COOLER'),
  ('Normal Delivery','NORMAL DELIVERY'),
)

STATUS_CHOICES=(
  ('Pending','PENDING'),
  ('Delivered','DELIVERED'),
  ('Cancelled','CANCELLED'),
  ('Accepted','ACCEPTED'),
  ('Reassigned','REASSIGNED'),
)

class Order(models.Model):
  UserID=models.ForeignKey(User, on_delete=models.CASCADE)
  DeliveryMethod=models.CharField(max_length=50, choices=DELIVERY_CHOICES)
  Phone=models.CharField(max_length=20)
  SenderName=models.CharField(max_length=50)
  Address1=models.CharField(max_length=250)
  Address2=models.CharField(max_length=250,null=True,blank=True)
  State=models.CharField(max_length=50)
  TodayDate=models.DateField(auto_now=True)
  DeliveryDate=models.DateField()
  Status=models.CharField(max_length=50, choices=STATUS_CHOICES,default="Pending")
  Reason=models.CharField(max_length=100,default="Empty",null=True,blank=True,unique=False)
  Charges=models.FloatField(default=0)
  Time=models.DateTimeField(auto_now=True)
  def __str__(self):
     return str(self.id)
  
class Item(models.Model):
  OrderID=models.ForeignKey(Order, on_delete=models.CASCADE)
  Image = models.ImageField(upload_to='images/')
  Price=models.FloatField()
  Description=models.CharField(max_length=250,null=True)
  PaymentMehtod=models.CharField(max_length=100,null=True,blank=True,default="Cash on Delivery")
  Time=models.DateTimeField(auto_now=True)
  def __str__(self):
     return str(self.id)

class Reciver(models.Model):
  OrderID=models.ForeignKey(Order, on_delete=models.CASCADE)
  Phone=models.CharField(max_length=20)
  SenderName=models.CharField(max_length=50)
  Address1=models.CharField(max_length=250)
  Address2=models.CharField(max_length=250,null=True,blank=True)
  State=models.CharField(max_length=50)
  Time=models.DateTimeField(auto_now=True)
  def __str__(self):
     return str(self.id)

DRIVER_ORDER_STATUS=(
  ('Accepted','ACCEPTED'),
  ('Pending','PENDING'),
  ('Delivered','DELIVERED'),
  ('Cancelled','CANCELLED'),
)
class Driver(models.Model):
  OrderID=models.ForeignKey(Order, on_delete=models.CASCADE)
  UserID=models.ForeignKey(User, on_delete=models.CASCADE)
  Status=models.CharField(max_length=50, choices=DRIVER_ORDER_STATUS,default="Pending")
  Reason=models.CharField(max_length=100,default="Empty",null=True,blank=True,unique=False)
  Time=models.DateTimeField(auto_now=True)
  def __str__(self):
     return str(self.id)
    
class Charges(models.Model):
  States=models.CharField(max_length=100)
  Charges=models.FloatField()
  Time=models.DateTimeField(auto_now=True)
  def __str__(self):
     return str(self.id)

class Reassign(models.Model):
  OrderID=models.ForeignKey(Order, on_delete=models.CASCADE)
  Status=models.CharField(max_length=50, choices=DRIVER_ORDER_STATUS,default="Pending")
  Time=models.DateTimeField(auto_now=True)
  def __str__(self):
     return str(self.id)
