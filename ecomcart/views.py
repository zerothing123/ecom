from django.shortcuts import render,redirect,get_object_or_404,HttpResponse

def index(request):
    return render(request,'ecomcart/base.html')