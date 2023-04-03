from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # return member name
    def __str__(self):
        return self.firstname


class CollectionCenter(models.Model):
    center_id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # return collection center name
    def __str__(self):
        return self.name
    
# Service Request Model

class ServiceRequest(models.Model):
    
    fullname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    

    # return collection center name
    def __str__(self):
        return self.fullname

# Collection Company Model

class CollectionCompany(models.Model):
    company_id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # return collection center name
    def __str__(self):
        return self.name
    
    # Reports Model

class Report(models.Model):
    member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    report_id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    issue = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # return collection center name
    def __str__(self):
        return self.name
    


   # Reports Model

class Feedback(models.Model):
    receiver = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, related_name='feedbacks')
    text = models.CharField(max_length=200, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)

    # return collection center name
    def __str__(self):
        return self.text
    
    
