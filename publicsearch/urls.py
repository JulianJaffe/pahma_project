__author__ = 'amywieliczka, jblowe'

from django.conf.urls import patterns, url
from publicsearch import views

urlpatterns = patterns('',
                       url(r'^(?i)search/?$', views.publicsearch, name='publicSearch'),
                       url(r'^(?i)results/?$', views.retrieveResults, name='retrieveResults'),
                       url(r'^(?i)bmapper/?$', views.bmapper, name='bmapper'),
                       url(r'^(?i)csv/?$', views.csv, name='csv'),
                       url(r'^(?i)gmapper/?$', views.gmapper, name='gmapper'),
                       )