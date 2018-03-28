# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from .models import *

# Create your views here.
def index(req):
    if req.session == True:
        req.session.clear()
    return render(req, 'appointments/index.html')

def create(req):
    errors = User.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/main')
    User.objects.create(name=req.POST['name'], email=req.POST['email'], password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()), birth = req.POST['birth'])
    req.session['active_name'] = User.objects.last().name
    req.session['active_id'] = User.objects.last().id
    return redirect('/appointments')

def login(req):
    errors = User.objects.login_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/main')
    loggedUser = User.objects.get(email = req.POST['email'])
    req.session['active_name'] = loggedUser.name
    req.session['active_id'] = loggedUser.id
    return redirect('/appointments')

def logoff(req):
    req.session.clear()
    return redirect('/main')

def appointments(req):
    current = datetime.datetime.now().date()
    now = datetime.datetime.strftime(current, '%Y-%m-%d')
    time_current = datetime.datetime.now()
    time_now = datetime.datetime.strftime(time_current, '%H:%M:%S')
    print time_now

    context = {
        'today': current,
        'time_now': time_now,
        'active_name': req.session['active_name'],
        'future_appointments': Appointment.objects.filter(appointee = User.objects.get(id=req.session['active_id'])).order_by('date', 'time'),
        'today_appointments': Appointment.objects.filter(appointee = User.objects.get(id=req.session['active_id'])).filter(date = now).order_by('time')
    }
    return render(req, 'appointments/appointments.html', context)

def add(req):
    errors = Appointment.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/appointments')
    Appointment.objects.create(task=req.POST['task'], date=req.POST['date'], time = req.POST['time'], appointee= User.objects.get(id=req.session['active_id']))
    return redirect('/appointments')

def delete(req, appointment_id):
    Appointment.objects.get(id = appointment_id).delete()
    return redirect('/appointments')

def edit(req, appointment_id):
    context = {
        'appointment': Appointment.objects.get(id=appointment_id),
    }
    return render(req, 'appointments/edit.html', context)

def update(req, appointment_id):
    errors = Appointment.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/appointments/{}/edit'.format(appointment_id))
    Appointment.objects.filter(id = appointment_id).update(task=req.POST['task'], status=req.POST['status'], date=req.POST['date'], time = req.POST['time'])
    return redirect('/appointments')