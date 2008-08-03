# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import simplejson

from django_orbited.models import Client


def destroy_clients(request):
    """Destroy Orbited clients from django_orbited models on unload
    browser event.
    """
    if request.POST and 'channels' in request.POST:
        channels = simplejson.loads(request.POST.get('channels'))
        session_key = request.session.session_key
        if 'id' in request.POST:
            user_id = simplejson.loads(request.POST.get('id'))
            user = get_object_or_404(User, id=user_id)
            clients = get_list_or_404(Client, session_key=session_key, \
                                      user=user, channel__in=channels)
        else:
            clients = get_list_or_404(Client, session_key=session_key, \
                                      channel__in=channels)
        for client in clients:
            client.delete()
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    else:
        return HttpResponseNotAllowed()
