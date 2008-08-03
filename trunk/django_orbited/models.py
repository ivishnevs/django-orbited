# -*- coding: utf-8 -*-
from pyorbited.simple import Client as OrbitedClient

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class ClientManager(models.Manager):
    """Perform sengins operations over users set
    """
    def send(self, data, channel):
        """Send message to all users suscribed to a channel
        """
        clients = Client.objects.filter(channel=channel)
        recipients = []
        for client in clients:
            recipients.append(client.get_recipient())
        client = OrbitedClient()
        if hasattr(settings, 'ORBITED_DISPATCH_PORT'):
            client.port = int(settings.ORBITED_DISPATCH_PORT)
        client.connect()
        body = {'channel': channel, 'body': data}
        response = client.event(recipients, body)
        client.disconnect()
        return response

    def multicast(self, data):
        """Send message to all users suscribed to a channel
        """
        responses = []
        clients = Client.objects.filter()
        for client in clients:
            responses.append(client.send(data))
        return responses


class Client(models.Model):
    channel = models.CharField(_('Channel'), max_length=250)
    callback = models.CharField(_('Callback function'), max_length=250)
    session_key = models.CharField(_('Session data'), max_length=150, null=True)

    user = models.ForeignKey(User, verbose_name=_('user'), null=True, blank=True)
    objects = ClientManager()

    def __unicode__(self):
        if self.user and self.user.id:
            return u"%s, channel %s on %s (%s)" % (self.user.username,
                                                   self.channel,
                                                   self.callback,
                                                   self.session_key)
        else:
            return u"channel %s on %s (%s)" % (self.channel,
                                               self.callback,
                                               self.session_key)

    def get_recipient(self):
        if self.user and self.user.id:
            recipient = "%s@%s, %s, /orbited" % (self.user.username, 
                                                 self.session_key, self.user.id)
        else:
            recipient = "AnonymousUser@%s, 0, /orbited" % (self.session_key)
        return recipient

    def send(self, data):
        client = OrbitedClient()
        if hasattr(settings, 'ORBITED_DISPATCH_PORT'):
            client.port = int(settings.ORBITED_DISPATCH_PORT)
        client.connect()
        recipient = self.get_recipient()
        body = {'channel': self.channel, 'body': data}
        response = client.event([recipient], body)
        client.disconnect()
        return response
