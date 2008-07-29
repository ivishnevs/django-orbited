# -*- coding: utf-8 -*-
from pyorbited.simple import Client as OrbitedClient

from django.conf import settings
from django.contrib.auth.models import User


class Client(object):
    def __init__(self, channel, callback=None, user=None, session_data=None):
        self.channel = channel
        if callback:
            self.callback = callback
        else:
            self.callback = "%s_callback" % (channel)
        if hasattr(settings, 'ORBITED_PROJECT_NAME'):
            project = settings.ORBITED_PROJECT_NAME
        else:
            project = ''
        if isinstance(user, User):
            username = user.username
        else:
            username = str(user)
        self.recipient = "%s@%s@%s, 0, /%s" \
                         % (project, username, session_data, channel)
        self.client = OrbitedClient()
        if hasattr(settings, 'ORBITED_PORT'):
            self.client.port = int(settings.ORBITED_PORT)

    def send(data, as_json=True):
        self.client.connect()
        self.client.event([self.recipient], data, json=as_json)
        self.client.disconnect()
