from django.conf.urls import patterns, url
from move import views

urlpatterns = patterns('',
                       url(r'^/?$', views.move_list, name='list'),
                       url(r'^move/?$', views.move, name='move'),
                       url(r'^power_move/?$', views.power_move, name='power_move'),
                       url(r'^sys_inv/?$', views.sys_inv, name='sys_inv'),
                       url(r'^sys_inv/update/?$', views.sys_inv_update, name='sys_inv_update'),
                       )
