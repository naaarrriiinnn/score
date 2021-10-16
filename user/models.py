from django.db import models
from account.models import CustomUser


# Create your models here.


class Person(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True)
    verified = models.BooleanField(default=False)
    scored = models.BooleanField(default=False)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_score = models.IntegerField()
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class Products(models.Model):
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="products")
    des = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname


class Scores(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
