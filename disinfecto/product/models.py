from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants as user_constants
from .managers import *


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()



class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile")
    phone = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email



class Product(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField()
    size = models.CharField(max_length=5, null=True, blank=True)
    colour = models.CharField(max_length=20, null=True, blank=True)
    price = models.FloatField()


    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user.email



class Feedback(models.Model):
    email = models.EmailField(max_length=100)
    description = models.TextField()


    def __str__(self):
        return self.email
