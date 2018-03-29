# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime
from datetime import time

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
    def basic_validator(self, postData, user_id):
        errors = {}
        now = datetime.now()
        form_dt = datetime.strptime("{}, {}".format(postData['date'], postData['time']), "%Y-%m-%d, %H:%M")
        appointments = Appointment.objects.filter(appointee = user_id)
        for appointment in appointments:
            appointment_dt = datetime.strptime("{}, {}".format(appointment.date, appointment.time), "%Y-%m-%d, %H:%M:%S")
            # print appointment_dt
            # print form_dt
            # print '-'*50
            if appointment_dt == form_dt:
                errors['duplicate_time'] = "Appointment already scheduled for that time!"
        if len(postData['task']) < 1:
            errors["empty_task"] = "Task cannot be empty!"
        if now > form_dt:
            errors["past_date"] = "Must select a current or future date and time!"
        return errors
class Appointment(models.Model):
    task = models.CharField(max_length=255)
    status = models.IntegerField(default = 1)
    date = models.DateField()
    time = models.TimeField()
    appointee = models.ForeignKey(User, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = AppointmentManager()

    def html_date(self):
        date_obj = self.date.__str__()
        return date_obj
    
    def html_time(self):
        time_obj = self.time.__str__()
        return time_obj
    
    def html_time_up(self):
        now = datetime.now()
        appointment_dt = datetime.strptime("{}, {}".format(self.date, self.time), "%Y-%m-%d, %H:%M:%S")
        # print appointment_dt
        if now > appointment_dt:
            return True
        else:
            return False