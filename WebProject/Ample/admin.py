from django.contrib import admin
from django.contrib.auth.models import User

from Ample.models import*
# Register your models here.
class classUserProfile(admin.ModelAdmin):
    list_display=['id','UserID','Image','UserType','Address','Time']

class classOrder(admin.ModelAdmin):
    list_display=['id','UserID','DeliveryMethod','Phone','SenderName','Address1','Address2','State','TodayDate','DeliveryDate','Status','Reason','Charges','Time']

class classitems(admin.ModelAdmin):
    list_display=['id','OrderID','Image','Price','Description','PaymentMehtod','Time']

class classReciver(admin.ModelAdmin):
    list_display=['id','OrderID','Phone','SenderName','Address1','Address2','State','Time']

class classDriver(admin.ModelAdmin):
    list_display=['id','OrderID','UserID','Status','Reason','Time']

class classCharges(admin.ModelAdmin):
    list_display=['id','States','Charges','Time']

class classsReassign(admin.ModelAdmin):
    list_display=['id','OrderID','Status','Time']


admin.site.register(UserProfile,classUserProfile)
admin.site.register(Order,classOrder)
admin.site.register(Item,classitems)
admin.site.register(Reciver,classReciver)
admin.site.register(Driver,classDriver)
admin.site.register(Charges,classCharges)
admin.site.register(Reassign,classsReassign)