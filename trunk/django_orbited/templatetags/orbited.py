# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.template import Context, Library, Node, TemplateSyntaxError
from django.template.loader import get_template

from django_orbited.models import Client

register = Library()

class OrbitedFilesNode(Node):
    """Include a script HTML tag in order to load Orbited Javascsript files.

    For example:
        {% orbited %}
   """
    def __repr__(self):
        return "<OrbitedFilesNode>"

    def render(self, context):
        port = None
        if hasattr(settings, 'ORBITED_PORT') and settings.ORBITED_PORT:
            port = settings.ORBITED_PORT
        socket_method = "orbited"
        if hasattr(settings, 'ORBITED_SOCKET_METHOD') \
        and settings.ORBITED_SOCKET_METHOD in ("BinaryTCPSocket", "TCPSocket", "WebSocket"):
            socket_method = settings.ORBITED_SOCKET_METHOD
        user = context.get('user', None)
        if user and user.id:
            username = user.username
            user_id = user.id
        else:
            username = 'AnonymousUser'
            user_id = 0
        session_key = context.get('session_key')
        recipient = "%s@%s, %s, /orbited" % (username, session_key, user_id)
        t = get_template('orbited_files.html')
        return t.render(Context({
                                 'port': port,
                                 'static_url': settings.ORBITED_STATIC_URL,
                                 'socket_method': socket_method,
                                 'user': user,
                                 'session_key': session_key,
                                 'recipient': recipient
                                }))

class OrbitedChannelNode(Node):
    """Include a script HTML tag in order to create Client objects.

    For example:
        {% orbited channel "channel_name" on "callback_javascript" %}
    """
    def __init__(self, channel, callback):
        self.channel = channel
        self.callback = callback

    def __repr__(self):
        return "<OrbitedChannelNode>"

    def render(self, context):
        user = context.get('user', None)
        if isinstance(user, AnonymousUser):
            user = None
        session_key = context.get('session_key')
        client, created = Client.objects.get_or_create(user=user,
                                                       channel=self.channel,
                                                       callback=self.callback,
                                                       session_key=session_key)
        client.save()
        t = get_template('orbited_channel.html')
        return t.render(Context({'client': client}))


def do_orbited(parser, token):
    bits = token.split_contents()
    bits_length = len(bits)
    if bits_length == 1:
        return OrbitedFilesNode()
    elif bits_length == 5 and bits[1] == 'channel' and bits[3] == 'on':
        cleaned_channel = bits[2]
        if cleaned_channel[0] in ("\"", "'") and cleaned_channel[-1] in ("\"", "'"):
            cleaned_channel = cleaned_channel[1:-1]
        cleaned_callback = bits[4]
        if cleaned_callback[0] in ("\"", "'") and cleaned_callback[-1] in ("\"", "'"):
            cleaned_callback = cleaned_callback[1:-1]
        return OrbitedChannelNode(cleaned_channel, cleaned_callback)
    else:
        raise TemplateSyntaxError, "%r tag requires no argument or channel " \
                                   "name and javascript callback function." \
                                   % token.contents.split()[0]

register.tag('orbited', do_orbited)
