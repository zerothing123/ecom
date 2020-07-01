from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=220,default="")
    title=models.CharField(max_length=220,default="")
    content=models.TextField()
    image=models.FileField(null=True,blank=True)
    category=models.CharField(max_length=550,default="")
    price=models.IntegerField(default=0)
    timstamp=models.DateTimeField(blank=True,default=now)

    def __str__(self):
        return self.title
    class Meta:
        ordering=['-timstamp']

class Review(models.Model):
    id=models.AutoField(primary_key=True)
    content=models.TextField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    parent=models.ForeignKey('self' ,on_delete=models.CASCADE,null=True)
    time=models.DateTimeField(blank=True,default=now)

    def __str__(self):
        return self.content

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    itemjson=models.TextField()
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=220,default="")
    email=models.CharField(max_length=300,default="")
    phone=models.CharField(max_length=255,default="")
    adress=models.TextField()
    thanks=models.BooleanField(default=False)

    def __str__(self):
        return self.name