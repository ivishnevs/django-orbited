from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^destroy/$', 'django_orbited.views.destroy_clients'),
    (r'^(.*)$', 'django.views.static.serve', {'document_root': settings.ORBITED_STATIC_PATH, 'show_indexes': True}),
)
