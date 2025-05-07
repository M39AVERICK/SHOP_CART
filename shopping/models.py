from django.db import models
from django.contrib.auth.models import User


class PRODUCT(models.Model):
    P_id=models.AutoField
    P_name=models.CharField(max_length=100)
    P_category=models.CharField(max_length=100,default='')
    p_sub=models.CharField(max_length=50,default='')
    P_desc=models.TextField(max_length=5000)
    p_price=models.IntegerField(default=0)
    p_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.P_name;

class Contact(models.Model):
    c_name=models.CharField(max_length=20)
    c_phone=models.IntegerField()
    c_email=models.EmailField()
    c_desc=models.TextField(max_length=500)

    def __str__(self):
        return self.c_name
    

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    temp_address = models.CharField(max_length=200)
    per_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    oid = models.CharField(max_length=50, blank=True)
    amountpaid = models.CharField(max_length=500, blank=True, null=True)
    paymentstatus = models.CharField(max_length=20, blank=True)
    phone = models.BigIntegerField(default=0)  # fixed from IntegerField with string default
    shipment_date = models.DateTimeField(null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # temporarily allow null

    def __str__(self):
        return f"{self.name} - Order #{self.order_id}"


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE,null=True, blank=True)
    delivered = models.BooleanField(default=False)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[:7] + "..."


# Create your models here.
