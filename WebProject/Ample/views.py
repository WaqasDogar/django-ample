from django.http import HttpResponseBadRequest
from django.contrib.auth  import authenticate,  login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from Ample.models import*
from random import randint

def random_with_N_digits():
    n=8
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
# Create your views here.

def GuestLogin(request):
    try:
        username=str(random_with_N_digits())
        pass1='12345'
        fname="GSTU_"+str(username)
        email=fname+"@gmail.com"
        # Create the user
        myuser = User.objects.create_user(username,email, pass1)
        myuser.first_name= fname
        myuser.save()
        UserProfile.objects.create(UserID=myuser,UserType="Guest",Address="")
        login(request,myuser,backend='django.contrib.auth.backends.ModelBackend')
        return redirect("UserProfile")

    except Exception as e:
        return render(request, 'Ample/login.html',{"msg":e})

# def ordersearch(request,result):

#     userinfo=UserProfile.objects.get(UserID=request.user)
#     return render(request,"Ample/ordersearch.html",{"userinfo":userinfo})

def getprice(orderID):
    odrid=Order.objects.get(id=orderID)
    rcvrid=Reciver.objects.get(OrderID=odrid)
    if odrid.State == "Out door areas" or rcvrid.State == "Out door areas":
        return Charges.objects.get(id=2).Charges
    if odrid.State != "Out door areas" and rcvrid.State != "Out door areas":
        return Charges.objects.get(id=1).Charges

def ReciverOrder(request,orderID):
    odrid=Order.objects.get(id=orderID)
    if Reciver.objects.filter(OrderID=odrid).count()>0:
        return HttpResponseBadRequest("Thanks! Your response is already done")

    if request.method=="POST":
        if request.POST.get("phone") is not None:
            odrid=Order.objects.get(id=orderID)
            Reciver.objects.create(OrderID=odrid,Phone=request.POST.get("phone"),SenderName=request.POST.get("name"),Address1=request.POST.get("addr1"),Address2=request.POST.get("addr2"),State=request.POST.get("state"))
            price=getprice(orderID)
            Order.objects.filter(id=orderID).update(Charges=float(price)+odrid.Charges)
            return redirect("Login")
    
    inc=False
    if odrid.Charges>0:
        inc=True

    return render(request,"Ample/newreciverorder.html",{"orderID":orderID,"inc":inc})

def orderchoice(request):
    return render(request,"Ample/orderchoice.html")

def UserCreateOrder(request):
    if request.method=="POST":
        if (request.POST.get("Delivery") is not None) and (request.POST.get("AED") is not None):
            obj=User.objects.get(username=request.user)
            price=0.0
            print("--------------------")
            print(request.POST.get("include"))
            if str(request.POST.get("include"))=="None":
                price=0.0
            elif str(request.POST.get("include"))=="on":
                price=float(request.POST.get("AED"))
            print("--------------------")
            orderID=Order.objects.create(UserID=obj,DeliveryMethod=request.POST.get("Delivery"),Phone=request.POST.get("phone"),SenderName=request.POST.get("name"),Address1=request.POST.get("addr1"),Address2=request.POST.get("addr2"),State=request.POST.get("state"),DeliveryDate=request.POST.get("ddate"),Charges=price)
            Item.objects.create(OrderID=orderID,Image=request.FILES["tasveer"],Price=request.POST.get("AED"),Description=request.POST.get("desc"))
            return render(request,"Ample/orderchoice.html",{"orderID":orderID})
    
    usr=UserProfile.objects.get(UserID=request.user)
    if usr.UserType=="Guest":
        return render(request,"Ample/neworder.html")
  
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/neworder.html",{"userinfo":userinfo})

def UProfile(request):
    if request.user.is_anonymous:
        return redirect("Login")

    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/profile.html",{"userinfo":userinfo})

def editprofile(request):
    if request.method=="POST":

        if request.POST.get("fullname") is not None:
            User.objects.filter(username=request.user).update(first_name=request.POST.get("fullname"),email=request.POST.get("email"),username=request.POST.get("phone"))
            UserProfile.objects.filter(UserID=request.user).update(Address=request.POST.get("address"))

        if request.FILES.get("tasveer") is not None:
            print("pic ayi ha")
            obj=UserProfile.objects.get(UserID=request.user)
            addr=obj.Address
            utype=obj.UserType
            obj.delete()
            UserProfile.objects.create(UserID=request.user,Image=request.FILES['tasveer'],UserType=utype,Address=addr)
            
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/editprofile.html",{"userinfo":userinfo})

def changepassword(request):
    if request.method=="POST":
        if request.POST.get("oldpass") is not None:
            user=authenticate(username= request.user, password= request.POST.get("oldpass"))
            if user is not None:
                if request.POST.get("pass1") ==request.POST.get("pass2"):
                    u=User.objects.get(username=request.user)
                    u.set_password(request.POST.get("pass1"))
                    u.save()
                    return redirect("Login")
                else:
                    userinfo=UserProfile.objects.get(UserID=request.user)
                    return render(request,"Ample/changepassword.html",{"userinfo":userinfo,"msg":"Passwords do not matched!"})
            else:
                userinfo=UserProfile.objects.get(UserID=request.user)
                return render(request,"Ample/changepassword.html",{"userinfo":userinfo,"msg":"Wrong old password"})

    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/changepassword.html",{"userinfo":userinfo})

def Login(request):
    try:
        if request.method=="POST":
            if request.POST.get("Phone"):
                phone=request.POST.get("Phone")
                pas=request.POST.get("pass")
                user=authenticate(username= phone, password= pas)
                userobject=UserProfile.objects.get(UserID=user)
                if user is not None and userobject.UserType=="Customer":
                    login(request,user)
                    return redirect("UserProfile")
                else:
                    return render(request, 'Ample/login.html',{'msg':"Wrong Credentials"})

        if request.user.is_authenticated and not request.user.is_staff:
            userobject=UserProfile.objects.get(UserID=request.user)
            if userobject.UserType=="Customer" or userobject.UserType=="Guest":
                return redirect("UserProfile")
            if userobject.UserType=="Driver":
                return redirect("driverdashboard")

        if request.user.is_authenticated and request.user.is_staff:
            userobject=UserProfile.objects.get(UserID=request.user)
            if userobject.UserType=="Admin":
                return redirect("admindashboard")

        return render(request,"Ample/login.html")
    except Exception as e:
        return render(request,"Ample/login.html",{'msg':e})

def Logout(request):
    logout(request)
    return redirect('Login')

def Signup(request):
    if request.method=="POST":
        if request.POST.get("phone") is not None:
            try:
                username=request.POST.get("phone")
                pass1=request.POST.get("pass1")
                pass2=request.POST.get("pass2")
                address=request.POST.get("address")
                email=request.POST.get("email")
                fname=request.POST.get("name")
                if (pass1!= pass2):
                    return render(request, 'Ample/signup.html',{"pas":"Passwords do not match"})
                # Create the user
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name= fname
                myuser.save()
                UserProfile.objects.create(UserID=myuser,UserType="Customer",Address=address)
                return redirect('Login')
            except Exception as e:
                return render(request, 'Ample/signup.html',{"pas":e})
        return render(request, 'Ample/signup.html',{"pas":"something went wrong! "})
    return render(request,"Ample/signup.html")

def previoususerorders(request):
    data=Order.objects.filter(UserID=request.user)
    if request.method=="POST":
        if request.POST.get("search") is not None:
            try:
                orderquery=request.POST.get("search")
                result=Order.objects.filter(id=orderquery,UserID=request.user)
                data=result
            except:
                pass

    return render(request,"Ample/previoususerdeliveries.html",{"Orders":data})

def userpendingdeliveries(request):
    data=Order.objects.filter(UserID=request.user,Status="Pending")
    return render(request,"Ample/userdeliveriespending.html",{"Orders":data})

def userdeliveriesdelivered(request):
    data=Order.objects.filter(UserID=request.user,Status="Delivered")
    return render(request,"Ample/userdeliveriesdelivered.html",{"Orders":data})

def usercancelleddeliveries(request):
    data=Order.objects.filter(UserID=request.user)
    return render(request,"Ample/usercancelleddeliveries.html",{"Orders":data})

#----------------admin views----------------------------------------

def adminlogin(request):
    try:
        if request.method=="POST":
            if request.POST.get("phone") is not None:
                phone=request.POST.get("phone")
                pas=request.POST.get("pass")
                user=authenticate(username= phone, password= pas)
                userobject=UserProfile.objects.get(UserID=user)
                if user is not None and userobject.UserType=="Admin":
                    login(request,user)
                    return redirect("admindashboard")
                else:
                    return render(request, 'Ample/adminlogin.html',{'msg':"Wrong Credentials"})

        if request.user.is_authenticated and request.user.is_staff:
            userobject=UserProfile.objects.get(UserID=request.user)
            if userobject.UserType=="Admin":
                return redirect("admindashboard")

        return render(request,"Ample/adminlogin.html")

    except Exception as e:
        return render(request, 'Ample/adminlogin.html',{'msg':e})

def admindashboard(request):
    if request.method=="POST":
        if request.POST.get("search") is not None:
            try:
                orderquery=request.POST.get("search")
                result=Order.objects.filter(id=orderquery)
                count=Order.objects.filter(id=orderquery).count()
                return render(request,"Ample/ordersearch.html",{"result":result,"search":request.POST.get("search"),"count":count})
            except:
                pass

    totalodr=Order.objects.count()
    odrpending=Order.objects.filter(Status="Pending").count()
    odrdelivered=Order.objects.filter(Status="Delivered").count()
    odrcancelled=Order.objects.filter(Status="Cancelled").count()

    odrlist=[totalodr,odrdelivered,odrcancelled,odrpending]

    ODR=Item.objects.all()
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/admindashboard.html",{"userprofile":userinfo,"ODR":ODR,"record":odrlist})

def customers(request):
    userinfo=UserProfile.objects.get(UserID=request.user)
    users=UserProfile.objects.filter(UserType="Customer")
    return render(request,"Ample/customers.html",{"userprofile":userinfo,"users":users})

def totalorder(request):
    userinfo=UserProfile.objects.get(UserID=request.user)
    ODR=Order.objects.all()
    return render(request,"Ample/totalorder.html",{"userprofile":userinfo,"ODR":ODR})

def completedorder(request):
    userinfo=UserProfile.objects.get(UserID=request.user)
    ODR=Driver.objects.filter(Status="Delivered")
    return render(request,"Ample/completedorder.html",{"userprofile":userinfo,"ODR":ODR})

def pendingorder(request):
    userinfo=UserProfile.objects.get(UserID=request.user)
    ODR=Driver.objects.filter(Status="Accepted")
    return render(request,"Ample/pendingorder.html",{"userprofile":userinfo,"ODR":ODR})

def cancelledorder(request):
    if request.method=="POST":
        if request.POST.get("reject") is not None:
            print("reason:"+str(request.POST.get("Reason")))
            Order.objects.filter(id=request.POST.get("OrderID")).update(Status="Cancelled By Admin",Reason=request.POST.get("Reason"))

    userinfo=UserProfile.objects.get(UserID=request.user)
    ODR=Driver.objects.all()
    return render(request,"Ample/cancelledorder.html",{"userprofile":userinfo,"ODR":ODR})

def addadmin(request):
    users=UserProfile.objects.filter(UserType="Admin")
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/admin.html",{"userprofile":userinfo,"users":users})

def createadmin(request):
    userinfo=UserProfile.objects.get(UserID=request.user)
    try:
        if request.method=="POST":
            if request.POST.get("phone") is not None:
                fname=request.POST.get("name") 
                email=request.POST.get("email") 
                username=request.POST.get("phone") 
                pass1=request.POST.get("pass1") 
                pass2=request.POST.get("pass2")  
                address=request.POST.get("addr") 
                if (pass1!= pass2):
                    return render(request, 'Ample/createadmin.html',{"msg":"Passwords do not match"})
                    # Create the user
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name= fname
                myuser.is_staff=True
                myuser.save()
                UserProfile.objects.create(UserID=myuser,UserType="Admin",Address=address,Image=request.FILES["tasveer"])
                return redirect('addadmin')

    except Exception as e:
        return render(request,"Ample/createadmin.html",{"userprofile":userinfo,"msg":e})

    return render(request,"Ample/createadmin.html",{"userprofile":userinfo})

def drivers(request):
    users=UserProfile.objects.filter(UserType="Driver")
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/drivers.html",{"userprofile":userinfo,"users":users})

def adddrivers(request):
    userinfo=UserProfile.objects.get(UserID=request.user)
    try:
        if request.method=="POST":
            if request.POST.get("phone") is not None:
                fname=request.POST.get("name") 
                email=request.POST.get("email") 
                username=request.POST.get("phone") 
                pass1=request.POST.get("pass1") 
                pass2=request.POST.get("pass2")  
                address=request.POST.get("addr") 
                if (pass1!= pass2):
                    return render(request, 'Ample/adddriver.html',{"pas":"Passwords do not match"})
                    # Create the user
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name= fname
                myuser.save()
                UserProfile.objects.create(UserID=myuser,UserType="Driver",Address=address,Image=request.FILES["tasveer"])
                return redirect('drivers')

    except Exception as e:
        return render(request,"Ample/adddriver.html",{"userprofile":userinfo,"msg":e})

    return render(request,"Ample/adddriver.html",{"userprofile":userinfo})

def charges(request):
    if request.method=="POST":
        Charges.objects.filter(States="State-to-State Charges (AED)").update(Charges=request.POST.get("Instate"))
        Charges.objects.filter(States="Out Door Areas Charges (AED)").update(Charges=request.POST.get("Outdoor"))

    statetostate=Charges.objects.get(States="State-to-State Charges (AED)")
    outdoor=Charges.objects.get(States="Out Door Areas Charges (AED)")

    return render(request,"Ample/Charges.html",{"instate":statetostate.Charges,"outdoor":outdoor.Charges})

def assignorder(request):
    if request.method=="POST":
        print(request.POST.get('OrderID'))
        print(request.POST.get('driverid'))
        odrid=request.POST.get('OrderID')
        drid=request.POST.get('driverid')
        if(request.POST.get('driverid')=='0'):
            driver=Driver.objects.all()
            ODRS=Order.objects.filter(Status="Pending")
            drivers=UserProfile.objects.filter(UserType="Driver")
            userinfo=UserProfile.objects.get(UserID=request.user)
            return render(request,"Ample/assignorder.html",{"userprofile":userinfo,"ODR":ODRS,"drivers":drivers,"Avail":driver,"msg":"(Please select the driver before saving!)"})
            
        oid=Order.objects.get(id=odrid)
        did=User.objects.get(username=drid)
        Driver.objects.create(OrderID=oid,UserID=did)
        
    driver=Driver.objects.all()
    ODRS=Order.objects.filter(Status="Pending")
    drivers=UserProfile.objects.filter(UserType="Driver")
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/assignorder.html",{"userprofile":userinfo,"ODR":ODRS,"drivers":drivers,"Avail":driver})

def reassignorder(request):
    msg=""
    if request.method=="POST":
        print(request.POST.get('OrderID'))
        print(request.POST.get('driverid'))
        odrid=request.POST.get('OrderID')
        drid=request.POST.get('driverid')
        if(request.POST.get('driverid')!='0'):
            oid=Order.objects.get(id=odrid)
            did=User.objects.get(username=drid)
            Driver.objects.create(OrderID=oid,UserID=did)
            Reassign.objects.filter(OrderID=oid).update(Status="Reassigned")

        elif (request.POST.get('driverid')=='0'):
            msg="(Please select the driver before saving!)"
        
    driver=Driver.objects.all()
    ODRS=Reassign.objects.all()
    drivers=UserProfile.objects.filter(UserType="Driver")
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/reassignorder.html",{"userprofile":userinfo,"ODR":ODRS,"drivers":drivers,"Avail":driver,"msg":msg})

def rebtn(request,id):
    odrid=Order.objects.get(id=id)
    Reassign.objects.create(OrderID=odrid,Status="Re-assign Required")
    return redirect("reassignorder")


#-----------------------Driver Views------------------------------------------

def driverlogin(request):
    try:
        if request.method=="POST":
            if request.POST.get("phone") is not None:
                phone=request.POST.get("phone")
                pas=request.POST.get("pass")
                user=authenticate(username= phone, password= pas)
                userobject=UserProfile.objects.get(UserID=user)
                if user is not None and userobject.UserType=="Driver":
                    login(request,user)
                    return redirect("driverdashboard")
                else:
                    return render(request, 'Ample/driverlogin.html',{'msg':"Wrong Credentials"})

        if request.user.is_authenticated:
            userobject=UserProfile.objects.get(UserID=request.user)
            if userobject.UserType=="Driver":
                return redirect("driverdashboard")

        return render(request,"Ample/driverlogin.html")

    except Exception as e:
        return render(request, 'Ample/driverlogin.html',{'msg':e})
    
def driverdashboard(request):
    if request.method=="POST":
        if request.POST.get("search") is not None:
            try:
                orderquery=request.POST.get("search")
                result=Driver.objects.filter(OrderID=orderquery,UserID=request.user)
                count=Driver.objects.filter(OrderID=orderquery,UserID=request.user).count()
                return render(request,"Ample/driverordersearch.html",{"result":result,"search":request.POST.get("search"),"count":count})
            except:
                pass

    totalodr=Driver.objects.filter(UserID=request.user).count()
    odrpending=Driver.objects.filter(Status="Pending",UserID=request.user).count()
    odrdelivered=Driver.objects.filter(Status="Delivered",UserID=request.user).count()
    odrcancelled=Driver.objects.filter(Status="Cancelled",UserID=request.user).count()
    odraccepted=Driver.objects.filter(Status="Accepted",UserID=request.user).count()
    Barlist=[totalodr,odrdelivered,odrcancelled,odrpending,odraccepted]
    
    obj=Driver.objects.filter(UserID=request.user)
    item=Item.objects.all()

    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/driverdashboard.html",{"userprofile":userinfo,"Barlist":Barlist,"odr":obj,"item":item})


def orderrequest(request):
    if request.method=="POST":
        if request.POST.get("accept") is not None:
            print(request.POST.get("OrderID"))
            print("accept command")
            Driver.objects.filter(id=request.POST.get("ID")).update(Status="Accepted")
            Order.objects.filter(id=request.POST.get("OrderID")).update(Status="Accepted")

        if request.POST.get("reject") is not None:
            print(request.POST.get("OrderID"))
            print(request.POST.get("Reason"))
            print("reject command")
            Driver.objects.filter(id=request.POST.get("ID")).update(Status="Cancelled",Reason=request.POST.get("Reason"))
            Order.objects.filter(id=request.POST.get("OrderID")).update(Status="Cancelled")


    obj=Driver.objects.filter(UserID=request.user,Status="Pending")
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/orderrequest.html",{"userprofile":userinfo,"ODR":obj})


def driveracceptedorder(request):
    odrs=Driver.objects.filter(UserID=request.user,Status="Accepted")
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/driveracceptedorder.html",{"userprofile":userinfo,"orders":odrs})

def DeliveredODR(request,id,orderid):
    Driver.objects.filter(id=id).update(Status="Delivered")
    Order.objects.filter(id=orderid).update(Status="Delivered")
    return redirect('driveracceptedorder')

def drivertotalorders(request):
    totalodr=Driver.objects.filter(UserID=request.user)
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/drivertotalorders.html",{"userprofile":userinfo,"totalorder":totalodr,"stat":"Total"})

def drivercompletedorder(request):
    odrdelivered=Driver.objects.filter(Status="Delivered",UserID=request.user)
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/drivertotalorders.html",{"userprofile":userinfo,"totalorder":odrdelivered,"stat":"Delivered"})

def drivercancelledorder(request):
    odrcancel=Driver.objects.filter(Status="Cancelled",UserID=request.user)
    userinfo=UserProfile.objects.get(UserID=request.user)
    return render(request,"Ample/drivertotalorders.html",{"userprofile":userinfo,"totalorder":odrcancel,"stat":"Cancelled"})


#---------------------------Order detail view------------------------------

def orderdetailview(request,orderid):
    try:
        ODR=Order.objects.get(id=orderid)
        ODRITEM=Item.objects.get(OrderID=orderid)
        ODRRECIVER=Reciver.objects.get(OrderID=orderid)
        return render(request,"Ample/viewdetails.html",{"ODR":ODR,"ODRITEM":ODRITEM,"ODRRECIVER":ODRRECIVER})
    except Exception as e:
        try:
            ODR=Order.objects.get(id=orderid)
            ODRITEM=Item.objects.get(OrderID=orderid)
            ODRRECIVER=e
            return render(request,"Ample/viewdetails.html",{"ODR":ODR,"ODRITEM":ODRITEM,"ODRRECIVER":ODRRECIVER,"msg":"(Reciver haven't provided information!!)"})
        except:
            return HttpResponseBadRequest("Order record doesn't exist its either deleted or remove...")