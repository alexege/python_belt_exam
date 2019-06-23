from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Createa an errors class to keep track of validation
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be of valid format'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        return errors

    def login_validator(self, postData):
        errors = {}

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be of valid format'
        if not User.objects.filter(email=postData['email']):
            errors['email'] = "Email address not recognized, please register if you haven't already done so."
        # if not User.objects.filter(password=postData['password']):
        #     errors['password'] = "Invalid password, please try again."
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        curr_date = str((datetime.now() - timedelta(days=1)))
        if len(postData['destination']) < 3:
            errors['destination'] = 'Destination must be at least 3 characters'
        if postData['start_date'] < curr_date:
            errors['start_date'] = "Time travel is not allowed. Start date can't be in the past"
        if postData['end_date'] < postData['start_date']:
            errors['end_date'] = "Time travel is not allowed. End date can't be before start date"
        if len(postData['plan']) < 3:
            errors['plan'] = 'Plan must be at least 3 characters'
        return errors

    def update_trip_validator(self, postData):
        errors = {}
        curr_date = str((datetime.now() - timedelta(days=1)))
        if len(postData['destination']) < 3:
            errors['destination'] = 'Destination must be at least 3 characters'
        if postData['start_date'] < curr_date:
            errors['start_date'] = "Time travel is not allowed. Start date can't be in the past"
        if postData['end_date'] < postData['start_date']:
            errors['end_date'] = "Time travel is not allowed. End date can't be before start date"
        if len(postData['plan']) < 3:
            errors['plan'] = 'Plan must be at least 3 characters'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"{self.id} {self.first_name}"

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="trips")
    users_joined = models.ManyToManyField(User, related_name="joined")

    objects = TripManager()

    def __repr__(self):
        return f"{self.id} {self.destination}"

