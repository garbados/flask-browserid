from flask.ext.login import login_user, logout_user
import requests
import flask
import json
import jinja2

class BrowserID(object):
    def __init__(self, app=None):
        self.views = flask.Blueprint('browserid', __name__, static_folder="static")

        self.views.before_app_request(self._load_auth_script)

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.login_url = app.config.get('BROWSERID_LOGIN_URL', '/api/login')
        self.logout_url = app.config.get('BROWSERID_LOGOUT_URL', '/api/logout')

        if not hasattr(self, 'login_callback') and hasattr(app, 'login_manager'):
            self.login_callback = app.login_manager.user_callback

        with self.views.open_resource('static/auth.js') as f:
            self.auth_script = jinja2.Template(f.read()).render(
                                    login_url=self.login_url, 
                                    logout_url=self.logout_url)

        self.views.add_url_rule(self.login_url, 
                                'login', 
                                self._login, 
                                methods=['POST'])
        self.views.add_url_rule(self.logout_url, 
                                'logout', 
                                self._logout, 
                                methods=['POST'])

        app.register_blueprint(self.views)

    def set_login_callback(self, func):
        """
        Registers a function that, given the response from the BrowserID servers,
        either returns a user, if login is successful, or None, if it isn't.
        """
        self.login_callback = func

    def set_logout_callback(self, func=None):
        """
        An optional callback to perform after logout.
        """
        if func:
            self.logout_callback = func

    def _load_auth_script(self):
        flask._request_ctx_stack.top.auth_script = self.auth_script

    def _login(self):
        payload = dict(
            assertion = flask.request.form['assertion'],
            audience = "http://localhost:5000")
        response = requests.post('https://browserid.org/verify', data=payload)
        if response.status_code == 200:
            user_data = json.loads(response.text)
            user = self.login_callback(user_data)
            if user:
                login_user(user)
                return ''
            else:
                if user_data.get('status') == "failure":
                    return flask.make_response(user_data['reason'], 400)
        else:
            return flask.make_response(response.text, response.status_code)

    def _logout(self):
        if hasattr(self,'logout_callback'):
            self.logout_callback()
        logout_user()
        return ''