from django.conf.urls import patterns, url
from public_facing_apps import views

urlpatterns = patterns('',
                       url(r'^/?$', views.list_apps, name='pfa'),
                       url(r'^collection_stats/$', views.collection_stats, name='collection_stats'),
                       )
