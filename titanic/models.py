from django.db import models

# Create your models here.
class Survivors(models.Model):
    pclass = models.IntegerField()
    survived = models.BooleanField()
    name = models.CharField(max_length=82, primary_key=True)
    sex = models.CharField(max_length=6)
    age = models.IntegerField()
    sibsp = models.IntegerField()
    parch = models.IntegerField()
    ticket = models.CharField(max_length=18)
    fare = models.DecimalField(max_digits=8, decimal_places=4)
    cabin = models.CharField(max_length=15)
    embarked= models.CharField(max_length=1)
    boat = models.CharField(max_length=7)
    body = models.IntegerField()
    homedest = models.CharField(max_length=50)
