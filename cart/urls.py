from django.contrib import admin
from django.urls import path
from . import  views

urlpatterns = [

    path('index/',views.loginuser,name="loginuser"),
    path('allprod/',views.allprod,name="allprod"),
    path('handlerequest/',views.handlerequest,name="handlerequest"),
    path('deleteprod/<int:id>',views.deleteProd,name="deleteProd"),
    path('deletereply/<int:id>',views.deletreply,name="deletreply"),
    path('deletecomment/<int:id>',views.Comdelete,name="Comdelete"),
    path('readmore/<int:id>',views.cusread,name="cusread"),
    path('review/',views.review,name="review"),
    path('checkout/',views.checkout,name="checkout"),
    path('error/',views.error,name="error"),
    path('create/',views.create,name="create"),
    path('view/<int:id>',views.viewprod,name="viewprod"),
    path('logout/',views.userlogout,name="userlogout"),
    path('landing/<str:name>',views.landing,name="landing"),
    path('search/',views.search,name="search"),
    path('signup/',views.signup,name="signup"),
    path('Signup/',views.Signup,name="Userlogin")
]