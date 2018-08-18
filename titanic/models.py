from django.db import models

# Create your models here.
class Survivors(models.Model):
    pclass = models.IntegerField()
    survived = models.BooleanField()
    name = models.CharField(max_length=82, primary_key=True)
    sex = models.CharField(max_length=6)
    age = models.IntegerField()
