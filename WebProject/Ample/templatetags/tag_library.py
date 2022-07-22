# templatetags/tag_library.py
from django import template
register = template.Library()
from django.contrib.auth.models import User
from Ample.models import *

@register.filter()
def to_int(value):
    return value.id

@register.filter()
def get_mail(value):
    obj=User.objects.all()
    for val in obj:
        if str(val)==str(value):
         return str(val.email)
         
@register.filter()
def to_str(value):
    return str(value)

@register.filter()
def get_user_pic(user):
    usr=UserProfile.objects.get(UserID=user)
    return usr.Image.url

@register.filter()
def fname(user):
    lst=str(user).split()
    return lst[0]

@register.filter()
def lname(user):
    lst=str(user).split()
    try:
        return lst[1]
    except:
        return ""

@register.filter()
def checkit(odrid):
    if Driver.objects.filter(OrderID=odrid).count()>0:
        return True
    return False

@register.filter()
def getdrivername(odrid):
    dvr=Driver.objects.get(OrderID=odrid)
    usr=User.objects.get(username=dvr.UserID) 
    return usr.first_name

@register.filter()
def getitemworth(ordid):
    itm=Item.objects.get(OrderID=ordid)
    return itm.Price