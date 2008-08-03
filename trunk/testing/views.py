# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext as _

from django_orbited.client import Client


#@login_required
def index(request):
#    print request.user
    return render_to_response('test.html',
                              {},
                              context_instance=RequestContext(request))
