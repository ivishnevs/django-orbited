# -*- coding: utf-8 -*-


def orbited(request):
    session_key = request.session.session_key
    return {'session_key': request.session.session_key}
