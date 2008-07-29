from os import environ
from sys import path

from config import map as config


def format_block(s):
    ''' Formatter for block strings to be sent as HTTP.
        (so they can be written cleanly in python classes)
    
        Dedent every line of a string by the indent of the first line,
        replace newlines with '\r\n', and remove any trailing whitespace.
    '''
    s = s.lstrip('\r\n').rstrip() # leading empty lines, trailing whitespace
    lines = s.expandtabs(4).splitlines()
    
    # find w, the smallest indent of a line with content
    w = min([len(line) - len(line.lstrip()) for line in lines])
    
    return '\r\n'.join([line[w:] for line in lines])

def is_authenticated_django_user(recipient):
    # TODO: Check authentication
    name = recipient.rsplit(",", 2)[0]
    name_split = name.split("@", 1)
    project = name_split[0]
    if project in config['django']:
        project_path = config['django'][project]
        path.append(project_path)
        from django.core.management import setup_environ
        import settings
        setup_environ(settings)
        print settings.ORBITED_PORT

    print recipient
    return True
