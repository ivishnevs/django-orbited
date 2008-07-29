from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^(.*)$', 'django.views.static.serve', {'document_root': settings.ORBITED_STATIC_PATH, 'show_indexes': True}),

)
