import logging
import urllib
import urllib2
from django.conf.urls import patterns, url
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse

# authorized_only decorator
from review_service.oauth.google import endpoints

def authorized_only(view_function):
    def wrapper(*args):
        # args[0] is request object, always.
        return authorize(view_function, args[0])

    return wrapper


def authorize(view_function, request):
    session = request.session
    if 'access_token' in session:
        if validate_token(session['access_token']):
            if 'user_info' not in session:
                write_user_info(session)
            if 'return_to' in session:
                return get_return_to(session)
            return view_function(request)

    session['return_to'] = request.get_full_path()
    return HttpResponseRedirect(get_auth_url())

# Callback for OAuth2
def handle_callback(request):
    code = request.GET.get('code')
    token = receive_token(code)

    if not validate_token(token):
        return HttpResponse(status=400)

    return HttpResponseRedirect(endpoints.CATCHTOKEN_URL + "/?token=" + token)


def catch_token(request):
    token = request.GET.get('token')
    request.session['access_token'] = token
    return get_return_to(request.session)


def validate_token(token):
    try:
        result = urllib2.urlopen(endpoints.TOKENINFO_URL + '?access_token=' + token)
        tokeninfo = json.loads(result.read())
        if('error' in tokeninfo) or (tokeninfo['audience'] != endpoints.CLIENT_ID):
            logging.warn('invalid access token = %s' % token)
            return False
        else:
            return True
    except urllib2.HTTPError, e:
        print e.code
        print e.msg
        print e.headers


def get_auth_url():
    params = get_params()
    return endpoints.AUTH_URL + '?' + urllib.urlencode(params)


def write_user_info(session):
    result = urllib2.urlopen(endpoints.USERINFO_URL + "/?access_token=" + session['access_token'])
    user_info = json.loads(result.read())
    session['user_info'] = user_info


def get_return_to(session):
    if 'return_to' in session:
        return_path = session['return_to']
        del session['return_to']
    else:
        return_path = ''
    return HttpResponseRedirect(endpoints.UNSAFE_ROOT_URL + return_path)


def receive_token(code):
    params = [('code', code),
        ('client_id', endpoints.CLIENT_ID),
        ('client_secret', endpoints.CLIENT_SECRET),
        ('redirect_uri', endpoints.REDIRECT_URL),
        ('grant_type', 'authorization_code')]
    result = urllib2.urlopen(endpoints.CODE_ENDPOINT, urllib.urlencode(params))
    content = json.loads(result.read())
    return content['access_token']


def get_params():
    return {
        'scope': endpoints.SCOPE,
        'state': '/profile',
        'redirect_uri': endpoints.REDIRECT_URL,
        'response_type': endpoints.RESPONSE_TYPE,
        'client_id': endpoints.CLIENT_ID
    }


def logout(request):
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'user_info' in request.session:
        del request.session['user_info']
    if 'return_to' in request.session:
        del request.session['return_to']
    return HttpResponse(status=200)
    #    return HttpResponseRedirect(endpoints.LOGOUT_URI) # This will logout user from Google


urls = patterns('',
    url(r'^logout/$', logout),
    url(r'^oauth2callback/$', handle_callback),
    url(r'^catchtoken/$', catch_token)
)