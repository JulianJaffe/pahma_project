from django.conf.urls import patterns, url
from info_review import views

urlpatterns = patterns('',
                       url(r'^/?$', views.info_review, name='info_review'),
                       url(r'^update/?$', views.update, name='update'),
                       )
