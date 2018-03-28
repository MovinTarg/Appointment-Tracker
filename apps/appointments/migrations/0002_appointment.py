# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-28 18:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=1)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('appointee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointments.User')),
            ],
        ),
    ]
