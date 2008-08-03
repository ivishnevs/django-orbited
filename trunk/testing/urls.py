from os import path
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Static content
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': path.join(settings.BASEDIR, 'media')}),
    (r'^orbited/', include('django_orbited.urls')),

    # Admin documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Django contrib
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^accounts/profile/$', 'views.index'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^admin/(.*)', admin.site.root),

    # Default
    (r'^$', 'views.index'),

)
