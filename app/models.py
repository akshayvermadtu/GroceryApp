from django.db import models
import jsonfield


class User(models.Model):
    name = models.CharField(max_length=20)
    phone = models.PositiveIntegerField(null=True)
    address = models.TextField()
    password = models.CharField(max_length=10)
    cart = jsonfield.JSONField(default={})

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=40)
    price = models.FloatField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=25)
    sub_category = models.CharField(max_length=25)
    brand = models.CharField(max_length=20)
    image = models.ImageField(upload_to="static/Images")

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_id = models.PositiveIntegerField(null=True)
    customer_name = models.CharField(max_length=30)
    customer_address = models.TextField()
    item_list = jsonfield.JSONField(default={})
    amount = models.FloatField(null=True)
    status = models.CharField(max_length=10)
    delivery_type = models.CharField(max_length=4, default='cod3')

    def __str__(self):
        return self.customer_address


class Offer(models.Model):
    image = models.ImageField(upload_to="static/OffersImages")
    url = models.CharField(max_length=20)

    def __str__(self):
        return self.image


class Structure(models.Model):
    category_name = models.CharField(max_length=50)
    sub_category_name = models.TextField()
    image = models.ImageField(upload_to="static/CatImages", default='static/CatImages/default_cat_icon.png')

    def __str__(self):
        return self.category_name
