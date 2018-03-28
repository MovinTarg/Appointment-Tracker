from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^appointments$', views.appointments),
    url(r'^logoff$', views.logoff),
    url(r'^add$', views.add),
    url(r'^appointments/(?P<appointment_id>\d+)/delete$', views.delete),
    url(r'^appointments/(?P<appointment_id>\d+)/edit$', views.edit),
    url(r'^appointments/(?P<appointment_id>\d+)/update$', views.update),
]
