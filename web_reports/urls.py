from django.conf.urls import patterns, url
from web_reports import views

urlpatterns = patterns('',
                       url(r'^/?$', views.list_apps, name='list'),
                       url(r'^hierarchy_viewer/$', views.hierarchy_viewer, name='hierarchy_viewer'),
                       url(r'^government_holdings/$', views.government_holdings, name='government_holdings'),
                       url(r'^packing_list/$', views.packing_list, name='packing_list'),
                       )
