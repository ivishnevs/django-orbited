# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

register = Library()

class OrbitedFilesNode(Node):
    """Include a script HTML tag in order to load Orbited Javascsript files.

    For example::
        {% orbited_files %}

    Or::
        {% orbited_files WebSocket %}
    """
    def __init__(self, method=None):
        if method in ("BinaryTCPSocket", "TCPSocket", "WebSocket"):
            self.method = method
        else:
            self.method = "orbited"

    def __repr__(self):
        return "<OrbitedFilesNode>"

    def render(self, context):
        if hasattr(settings, "ORBITED_PORT") and settings.ORBITED_PORT:
            port_script = """
<script type="text/javascript" language="javascsript">
ORBITED_PORT = %s;
</script>""" % settings.ORBITED_PORT
        else:
            port_script = ""
        output_script = """
<script type="text/javascript" language="javascsript"
        src="%s%s.js">
</script>%s""" % (settings.ORBITED_STATIC_URL, self.method, port_script)
        return output_script

def do_orbited_files(parser, token):
    bits = token.split_contents()
    bits_length = len(bits)
    if bits_length == 1:
        return OrbitedFilesNode()
    elif bits_length == 2:
        return OrbitedFilesNode(bits[1])
    else:
        raise TemplateSyntaxError, "%r tag requires no argument or socket type argument." \
                                   % token.contents.split()[0]

register.tag('orbited_files', do_orbited_files)
