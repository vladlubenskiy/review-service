import os

# Google's OAuth 2.0 endpoints
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
CODE_ENDPOINT = "https://accounts.google.com/o/oauth2/token"
TOKENINFO_URL = "https://accounts.google.com/o/oauth2/tokeninfo"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
SCOPE = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
LOGOUT_URI = 'https://accounts.google.com/logout'

# client ID / secret & cookie key
CLIENT_ID = '219211176840.apps.googleusercontent.com'
CLIENT_SECRET = 'PitmLoQjvrjnuofnfj8iN1qq'
COOKIE_KEY = os.urandom(64)

is_secure = os.environ.get('HTTPS') == 'on'
protocol = {False: 'http', True: 'https'}[is_secure]

SECURE_ROOT_URL = protocol + '://localhost:8002'
UNSAFE_ROOT_URL = "http://localhost:8003"
RESPONSE_TYPE = 'code'
REDIRECT_URL = 'https://localhost:8002/auth/oauth2callback/'
CATCHTOKEN_URL = SECURE_ROOT_URL + '/auth/catchtoken'