from django.conf.urls import patterns, url
from inventory import views

urlpatterns = patterns('',
                       url(r'^/?$', views.inventory, name='inventory'),
                       url(r'^update/?$', views.update, name='update'),
                       )
