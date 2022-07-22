from django.urls import path
from Ample import views

urlpatterns = [

    #-----------Customer Urls------------------------------
    path('',views.Login,name='Login'),
    path('Signup/',views.Signup,name='Signup'),
    path('UserProfile/',views.UProfile,name='UserProfile'),
    path('UserCreateOrder/',views.UserCreateOrder,name='UserCreateOrder'),
    path('ReciverOrder/<str:orderID>',views.ReciverOrder,name='ReciverOrder'),
    path('orderchoice/',views.orderchoice,name='orderchoice'),
    path('logout/',views.Logout,name='logout'),
    path('previoususerorders/',views.previoususerorders,name='previoususerorders'),
    path('userpendingdeliveries/',views.userpendingdeliveries,name='userpendingdeliveries'),
    path('userdeliveriesdelivered/',views.userdeliveriesdelivered,name='userdeliveriesdelivered'),
    path('usercancelleddeliveries/',views.usercancelleddeliveries,name='usercancelleddeliveries'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    
    #---------------Admin urls-------------------------------

    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('admindashboard',views.admindashboard,name='admindashboard'),
    path('customers',views.customers,name='customers'),
    path('totalorder',views.totalorder,name='totalorder'),
    path('completedorder',views.completedorder,name='completedorder'),
    path('pendingorder',views.pendingorder,name='pendingorder'),
    path('cancelledorder',views.cancelledorder,name='cancelledorder'),
    path('addadmin',views.addadmin,name='addadmin'),
    path('createadmin',views.createadmin,name='createadmin'),
    path('drivers',views.drivers,name='drivers'),
    path('adddrivers',views.adddrivers,name='adddrivers'),
    path('assignorder',views.assignorder,name='assignorder'),
    path('reassignorder',views.reassignorder,name='reassignorder'),
    path('rebtn/<str:id>',views.rebtn,name='rebtn'),
    path('Charges',views.charges,name='Charges'),

    #---------------Driver urls------------------------------
    
    path('driverlogin/',views.driverlogin,name='driverlogin'),
    path('driverdashboard/',views.driverdashboard,name='driverdashboard'),
    path('orderrequest/',views.orderrequest,name='orderrequest'),
    path('driveracceptedorder/',views.driveracceptedorder,name='driveracceptedorder'),
    path('DeliveredODR/<str:id>/<str:orderid>',views.DeliveredODR,name='DeliveredODR'),
    path('drivertotalorders/',views.drivertotalorders,name='drivertotalorders'),
    path('drivercompletedorder/',views.drivercompletedorder,name='drivercompletedorder'),
    path('drivercancelledorder/',views.drivercancelledorder,name='drivercancelledorder'),
    
    #-----------------Order details view urls-----------------------
    path('orderdetailview/<str:orderid>',views.orderdetailview,name='orderdetailview'),

    #-----------------Guest Login------------------------------------
    path('GuestLogin/',views.GuestLogin,name='GuestLogin'),

    #---------------- Order Search-----------------------------------
    #path('ordersearch/<str:result>',views.ordersearch,name='ordersearch'),

]