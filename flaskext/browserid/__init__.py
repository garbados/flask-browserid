from flask.ext.login import login_user, logout_user
import requests
import flask
import json
import jinja2

class BrowserID(object):
    def __init__(self, app=None, **kwargs):
        self.views = flask.Blueprint('browserid', __name__, static_folder="static")
        self.login_url = kwargs['login_url'] if kwargs.has_key('login_url') else '/api/login'
        self.login_callback = kwargs['login_callback'] if kwargs.has_key('login_callback') else None
        self.logout_url = kwargs['logout_url'] if kwargs.has_key('logout_url') else '/api/logout'
        self.logout_callback = kwargs['logout_callback'] if kwargs.has_key('logout_callback') else None

        self.views.add_url_rule(login_url, 'login', self._login)
        self.views.add_url_rule(logout_url, 'logout', self._logout)

        with views.open_resource('static/auth.js') as f:
            self.auth_script = jinja2.Template(f.read()).render(
                                    login_url=login_url, 
                                    logout_url=logout_url)

        views.before_app_request(self._load_auth_script)

        if app:
            app.register_blueprint(self.views)

    def init_app(app, **kwargs):
        super(BrowserID, self).__init__(app, **kwargs)

    def _load_auth_script(self):
        flask._request_ctx_stack.top.auth_script = self.auth_script

    def _login(self):
        payload = dict(
            assertion = flask.request.form['assertion'],
            audience = "http://localhost:5000")
        response = requests.post('https://browserid.org/verify', data=payload)
        if response.status_code == 200:
            user_data = json.loads(response.text)
            if self.login_callback:
                self.login_callback(user_data)
            login_user(user)
            return ''
        else:
            return flask.make_response(response.text, response.status_code)

    def _logout(self):
        if self.logout_callback:
            self.logout_callback()
        logout_user()
        return ''