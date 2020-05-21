from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family_members = models.IntegerField()

    class Meta:
        verbose_name = ("customer")
        verbose_name_plural = ("customers")
    
