import unittest
import flask
from flask.ext.login import LoginManager, UserMixin
from flaskext.browserid import BrowserID
import sys

class User(UserMixin):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')

USERS = [
    User(email="test@test.test", id=1),
    User(email="test2@est.test", id=2),
    ]

def get_user_by_id(id):
    for user in USERS:
        if unicode(user.id) == id:
            return user
    else:
        return None

def create_browserid_user(kwargs):
    """
    takes browserid response and creates a user.
    """
    if kwargs['status'] == 'okay':
        id = max([user.id for user in USERS]) + 1
        user = User(email = kwargs['email'], id = id)
        USERS.append(user)
        return user
    else:
        return None

def get_user(kwargs):
    # try to find the user
    for user in USERS:
        if user.email == kwargs.get('email') or user.id == kwargs.get('id'):
            return user
    # try to create the user
    return create_browserid_user(kwargs)
    
def index():
    return flask.render_template('index.html')

def generate_app():
    app = flask.Flask(__name__)

    app.config['BROWSERID_LOGIN_URL'] = "/login"
    app.config['BROWSERID_LOGOUT_URL'] = "/logout"
    app.config['SECRET_KEY'] = "deterministic"
    app.config['TESTING'] = True

    login_manager = LoginManager()
    login_manager.user_loader(get_user_by_id)
    login_manager.init_app(app)

    browserid = BrowserID()
    browserid.user_loader(get_user)
    browserid.init_app(app)
    
    app.route('/')(index)
    
    return app

class BasicAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = generate_app()
        self.client = self.app.test_client()
        self.login_manager = self.app.login_manager
        self.browserid = self.app.browserid
        self.login_url = self.app.config['BROWSERID_LOGIN_URL']
        self.logout_url = self.app.config['BROWSERID_LOGOUT_URL']

    def test_login(self):
        # bad login
        res = self.client.post(self.login_url, data={'assertion' : 'ducks'})
        assert res.status_code == 500
        # todo: good login

    def test_logout(self):
        # todo: log user in, test that user is actually logged out
        # good logout
        res = self.client.post(self.logout_url)
        assert res.status_code == 200

    def test_static_file(self):
        # todo: test that "auth.js" is compiled and 
        # available in the request contexts
        pass
        
    def test_multiple_applications(self):
        """
        ensures that the extension supports multiple applications.
        """
        new_app = generate_app()
        assert self.app != new_app

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        generate_app().run()
    else:
        unittest.main()
