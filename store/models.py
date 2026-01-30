from django.db import models
from django.contrib.sessions.models import Session
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True)
    description = models.TextField()
    image = models.ImageField() #Must install Pillow library
    pdf_file = models.FileField(null=True)
    price = models.FloatField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Category = models.ForeignKey(Category, on_delete=models.PROTECT) #Prevent delete the category when deleting the product
    author = models.ForeignKey(Author, on_delete=models.SET_NULL , null=True) #When delete the author, its field set to null #review IPAM Project for user field in ipaddress model!
    def __str__(self):
        return self.name
    
    @property
    def pdf_file_url(self):
        return settings.SITE_URL + self.pdf_file.url

class Order(models.Model):
    customer = models.JSONField(default=dict) #default=empty dictionary {}
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    
    @property
    def customer_name(self):
        return f"{self.customer['first_name']} {self.customer['last_name']}"

class OrderProduct(models.Model):
        order = models.ForeignKey(Order, on_delete=models.PROTECT)
        Product = models.ForeignKey(Product, on_delete=models.PROTECT)
        price = models.FloatField()
        created_at = models.DateTimeField(auto_now_add=True)

class Slider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(max_length=255)
    image = models.ImageField(null=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    items = models.JSONField(default=dict) #will stores Products that exist in the cart
    session = models.ForeignKey(Session , on_delete=models.CASCADE) #When the session is deleted, whole the cart will be deleted