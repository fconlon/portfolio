from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ParentToChildren(models.Model):
    parent = models.CharField(max_length=50)
    child = models.ForeignKey(User, on_delete=models.CASCADE)
    
class ChildToParents(models.Model):
    child = models.CharField(max_length=50)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    
class AllowanceUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_parent = models.BooleanField()
    balance = models.DecimalField(max_digits=7, decimal_places=2)