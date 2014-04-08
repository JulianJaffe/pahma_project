from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views

admin.autodiscover()

#
# Initialize our web site -things like our AuthN backend need to be initialized.
#
from main import cspace_django_site

cspace_django_site.initialize()

urlpatterns = patterns('',
                       #  Examples:
                       #  url(r'^$', 'cspace_django_site.views.home', name='home'),
                       #  url(r'^cspace_django_site/', include('cspace_django_site.foo.urls')),

                       #  Uncomment the admin/doc line below to enable admin documentation:
                       #  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^(?i)admin/?', include(admin.site.urls)),
                       url(r'^/?$', 'hello.views.home', name='home'),
                       url(r'^(?i)service/?', include('service.urls')),
                       url(r'^(?i)accounts/login/?$', views.login, name='login'),
                       url(r'^(?i)accounts/logout/?$', views.logout_then_login, name='logout'),
                       url(r'^(?i)search/?', include('publicsearch.urls', namespace='publicsearch')),
                       url(r'^(?i)ireports/?', include('ireports.urls', namespace='ireports')),
                       url(r'^(?i)imageserver/?', include('imageserver.urls', namespace='imageserver')),
                       url(r'^(?i)imagebrowser/?', include('imagebrowser.urls', namespace='imagebrowser')),
                       url(r'^(?i)uploadmedia/?', include('uploadmedia.urls', namespace='uploadmedia')),
                       )
