from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class User(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=False, null=False)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    password = models.CharField(max_length=256, blank=False, null=False)
    phone = models.CharField(max_length=45, blank=False, null=False)

    def __str__(self):
        return self.name or "No name"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
    

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
  
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name