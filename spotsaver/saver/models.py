from django.db import models
import re, bcrypt

from django.db.models.manager import Manager
from datetime import datetime

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_n'])<2:
            errors['f_n']="First name must be longer than 2 characters!"
        if len(postdata['l_n'])<2:
            errors['l_n']="Last name must be longer than 2 characters!"
        if not email_check.match(postdata['email']):
            errors['email']="Email must be valid format!"
        if len(postdata['pw'])<8:
            errors['pw']="Password must be at least 8 characters!"
        if postdata['pw'] != postdata['conf_pw']:
            errors['conf_pw']="Password and confirm password must match!"
        return errors   

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class SpaceManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData.get("location")) < 5:
            errors["location"] = "Location must be more than 5 characters long"
            return errors
        if len(postData["description"]) < 5:
            errors["description"] = "Description must be longer than 5 characters"
            return errors

class Space(models.Model):
    location = models.CharField(max_length=255)
    description = models.TextField()
    spot_num= models.CharField(max_length=255)
    spot = models.ManyToManyField(User, related_name="spot")
    author = models.ForeignKey(User, related_name= "author", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SpaceManager()
