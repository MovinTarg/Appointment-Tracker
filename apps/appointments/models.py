# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        current = datetime.datetime.now().date()
        now = datetime.datetime.strftime(current, '%Y-%m-%d')
        users = User.objects.all()
        for user in users:
            if user.email == postData['email']:
                errors['duplicate_email'] = "Email already in database"
        if len(postData['email']) < 1:
            errors["empty_email"] = "Email cannot be empty!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "Invalid Email Address!"
        if len(postData['name']) < 3:
            errors["empty_name"] = "First name must be at least 3 characters long!"
        if any(i.isdigit() for i in postData['name']) == True:
            errors["invalid_name"] = "Invalid first name!"
        if len(postData['password']) < 8:
            errors["short_password"] = "Password must contain at least eight characters!"
        if postData['confirm_password'] != postData['password']:
            errors["password_does_not_match"] = "Passwords must match!"
        if now <= postData['birth']:
            errors["future_birth"] = "Must select a date of birth before today!"
        return errors
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email=postData['email']):
            errors['unregistered'] = "Invalid Email!"
        else:
            user = User.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == True:
                pass
            else:
                errors['invalid_password'] = "Invalid Password!"
        return errors
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class AppointmentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        current = datetime.datetime.now().date()
        now = datetime.datetime.strftime(current, '%Y-%m-%d')
        time_current = datetime.datetime.now()
        time_now = datetime.datetime.strftime(time_current, '%H:%M:%S')
        appointment_time = str(postData['time'])+':00'
        apt_time = datetime.datetime.strftime(appointment_time, '%H:%M:%S')
        print apt_time
        
        appointments = Appointment.objects.all()
        for appointment in appointments:
            print '-----'
            print appointment.date
            print appointment.time
            if appointment.date == postData['date'] and appointment.time == apt_time:
                errors['duplicate_time'] = "Appointment already scheduled for that time!"
        if len(postData['task']) < 1:
            errors["empty_task"] = "Task cannot be empty!"
        if now > postData['date']:
            errors["past_date"] = "Must select a current or future date!"
        if time_now > postData['time']:
            errors["past_time"] = "Must select a future time!"
        return errors
class Appointment(models.Model):
    task = models.CharField(max_length=255)
    status = models.IntegerField(default = 1)
    date = models.DateField()
    time = models.TimeField('%H:%M')
    appointee = models.ForeignKey(User, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = AppointmentManager()