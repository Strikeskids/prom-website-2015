import api

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, static_path='/')
app.wsgi_app = ProxyFix(app.wsgi_app)

session_cookie_domain = '127.0.0.1'
session_cookie_path = '/'
session_cookie_name = 'flask'
secret_key = ''

def config_app(*args, **kwargs):

    app.secret_key = secret_key
    app.config.update({
        'SESSION_COOKIE_DOMAIN': session_cookie_domain,
        'SESSION_COOKIE_NAME': session_cookie_name,
        'SESSION_COOKIE_PATH': session_cookie_path,    
    })

    app.register_blueprint(api.routes.blueprint, url_prefix='/api')

    return app

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, *')
    response.headers.add('Cache-Control', 'no-cache')
    response.headers.add('Cache-Control', 'no-store')
    if api.auth.is_logged_in():
        if 'token' in session:
            response.set_cookie('token', session['token'])
        else:
            csrf_token = api.common.token()
            session['token'] = csrf_token
            response.set_cookie('token', csrf_token)

    response.mimetype = 'application/json'
    return response
