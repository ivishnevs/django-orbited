from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('django_orbited.views',
    (r'^destroy/$', 'destroy_clients'),
)

urlpatterns += patterns('django.views',
    (r'^(.*)$', 'static.serve', {'document_root': settings.ORBITED_STATIC_PATH, 'show_indexes': True}),
)
