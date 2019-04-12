from django.db import models
from datetime import datetime
from realtors.models import Seller, Realtor
from django.contrib.auth.models import User


# Create your models here.
class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathroom = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    photo_main = models.ImageField(upload_to='photos/%y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateField(default=datetime.now,blank=True)
    def __str__(self):
        return self.title


PRODUCT_TYPE = {
    ('Mobile', 'Mobile'),
    ('Laptop', 'Laptop'),
}

product_sub_type = {
    ('Electronic_product', 'Electronic_product'),
    ('accessories', 'accessories'),
}
brand_name = {
    ('Onepluse', 'Onepluse'),
    ('Hp', 'Hp'),
    ('Dell', 'Dell'),
    ('Apple', 'Apple'),
}

class Product(models.Model):
    seller = models.ForeignKey(Seller , on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, choices=brand_name)
    type = models.CharField(max_length=200, choices=PRODUCT_TYPE)
    sub_type = models.CharField(max_length=100, choices=product_sub_type)
    #zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    ram = models.IntegerField(blank=True)
    processor = models.CharField(max_length=100,blank=True)
    storage = models.DecimalField(max_digits=6, decimal_places=1,blank=True)
    processor_spped = models.DecimalField(max_digits=6, decimal_places=1,blank=True)
    display_size = models.DecimalField(max_digits=5, decimal_places=2,blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=1,blank=True)
    photo_main = models.ImageField(upload_to='photos/%y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%y/%m/%d/', blank=True)
    is_available = models.BooleanField(default=True)
    list_date = models.DateField(default=datetime.now,blank=True)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    products = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


