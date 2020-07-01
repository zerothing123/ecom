from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.admin import  User
from .models import Product,Review,Order
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .paytm import  checksome
MERCHANT_KEY='K7j!AHRC@i1AI61H'
# Create your views here.
def loginuser(request):
    if request.method=="POST":
        name=request.POST.get('name')
        password=request.POST.get('password')
        user=authenticate(username=name,password=password)
        if user is not None :
            login(request,user)
            return redirect(f'/cart/landing/{request.user}')
        else:
            return redirect('/cart/error/')
    return render(request,'cart/index.html')
def landing(request,name):
    obj=Product.objects.filter(name=name)
    return render(request,'cart/landing.html',{'obj':obj})
def create(request):
    if request.method=="POST":
        title=request.POST.get('title')
        name=request.POST.get('name')
        content=request.POST.get('content')
        cat=request.POST.get('cat')
        image=request.FILES.get('image')
        price=request.POST.get('price')
        form=Product(name=name,title=title,content=content,image=image,category=cat,price=price)
        if form=="":

            return redirect(f'/cart/landing/{request.user}')
        else:
            form.save()
            return redirect(f'/cart/landing/{request.user}')
    return render(request,'cart/create.html')
def review(request):
    if request.method=="POST":
        content=request.POST.get('review')
        replycontent = request.POST.get('replytxt')
        productid=request.POST.get('product')
        productparent=Product.objects.get(id=productid)
        # print(productparent)
        replyparentid=request.POST.get('replyid')  #we also have to add this hiiden field in the comment form as well
        if replyparentid=="":
            form=Review(content=content,product=productparent)

            form.save()
            return redirect(f'/cart/readmore/{productid}')
        else:
            parentComment=Review.objects.get(id=replyparentid)
            # print(parentComment)
            form=Review(content=replycontent,product=productparent,parent=parentComment)
            form.save()
            return redirect(f'/cart/readmore/{productid}')

    return redirect(f'/cart/readmore/{Product.id}')
def checkout(request):
    if request.method=="POST":
        itemjson=request.POST.get('itemjson')
        amount=request.POST.get('newtag')
        name=request.POST.get("name")
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        adress=request.POST.get('adress')
        order=Order(itemjson=itemjson,name=name,email=email,phone=phone,adress=adress,amount=amount)
        thanks = True

        order.save()
        orderid=order.id
        print(orderid)
        data_dict = {
            'MID': 'MEYuTp32745711695706',
            'ORDER_ID': str(orderid),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/cart/handlerequest/',
        }
        data_dict['CHECKSUMHASH']=checksome.generate_checksum(data_dict,MERCHANT_KEY)
        return render(request, 'cart/payment.html',{'thanks':thanks,'id':orderid,'data_dict':data_dict})
    return render(request,'cart/checkout.html')

@csrf_exempt
def handlerequest(request):
    form =request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]
    verify=checksome.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print('order succesfull')
        else:
            print('orde not succesfull'+response_dict['RESPMSG'])
    return render(request,'cart/paymentStatus.html',{'response':response_dict})

def search(request):
    querry=request.GET['search']

    obj=Product.objects.filter(Q(title__icontains=querry)|Q(content__icontains=querry)|Q(category__icontains=querry))
    if obj:
        param={'product':obj}
        return render(request, 'cart/search.html', param)

    param = {'obj1': querry}
    return render(request, 'cart/search.html', param)
def Comdelete(request,id):
    obj = Review.objects.filter(id=id)
    object=request.GET.get('object',"")
    obj.delete()
    return redirect(f'/cart/readmore/{object}')
def deletreply(request,id):
    obj=Review.objects.filter(id=id)
    prod=request.GET.get('productid',"")
    obj.delete()
    return redirect(f'/cart/readmore/{prod}')
def deleteProd(request,id):
    obj=Product.objects.filter(id=id)
    name=request.GET.get('name',"")
    obj.delete()
    return redirect(f'/cart/landing/{name}')
def viewprod(request,id):
    obj=Product.objects.filter(id=id).first()
    # obj2 = Product.objects.filter(category=obj.category)
    adminreview=Review.objects.filter(product=obj,parent=None)
    reply = Review.objects.filter(product=obj).exclude(parent=None)
    replydict = {}
    print(reply)
    for i in reply:
        print(i)
        if i.parent.id not in replydict.keys():
            replydict[i.parent.id] = [i]
        else:
            replydict[i.parent.id].append(i)
    print(replydict)
    # print(obj.category)
    # obj1=Product.objects.filter(category=obj.category)
    return render(request,'cart/view.html',{'obj1':obj,'review':adminreview,'reply':replydict})
def cusread(request,id):
    obj=Product.objects.filter(id=id).first()
    obj2=Product.objects.filter(category=obj.category)
    reviews=Review.objects.filter(product=obj,parent=None)
    reply=Review.objects.filter(product=obj).exclude(parent=None)
    replydict={}
    print(reply)
    for i in reply:
        print(i)
        if i.parent.id not in replydict.keys():
            replydict[i.parent.id]=[i]
        else:
            replydict[i.parent.id].append(i)
    print(replydict)
    return render(request,'cart/readmorecust.html',{'obj':obj,'cat':obj2,'review':reviews,'reply':replydict})
def allprod(request):
    obj=Product.objects.all()
    return render(request,'cart/allprod.html',{'obj':obj})
def signup(request):
    return render(request,'cart/signup.html')
def error(request):
    return render(request,'cart/error.html')
def Signup(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if len(name)>20:
            raise ValueError('name has to be less than 20char')
        if password!=pass2:
            raise ValueError('passwords need to match')
        else:
            user=User.objects.create_user(name,email,password)
            user.save()
        return redirect('/cart/index/')
def userlogout(request):
    logout(request)
    return redirect('/cart/index/')