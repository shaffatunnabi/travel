from django.db import models

class Person(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    age = models.IntegerField()

def __str__(self):
    return self.username

class Book(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    numpeople = models.CharField(max_length=100)

def __str__(self):
    return self.name
