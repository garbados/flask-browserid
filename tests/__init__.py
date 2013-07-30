import flask
from flask.ext.login import LoginManager, UserMixin
from flaskext.browserid import BrowserID
import sys
import unittest

## SETUP
class User(UserMixin):
    """
    Test user class
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')

USERS = [
    User(email="test@test.test", id=1),
    User(email="test2@est.test", id=2),
    ]

def get_user_by_id(id):
    """
    Given a unicode ID, returns the user that matches it.
    """
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
    """
    Given the response from BrowserID, finds or creates a user.
    If a user can neither be found nor created, returns None.
    """
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

class Tests(unittest.TestCase):
    def setUp(self):
        self.app = generate_app()

    def test_login(self):
        app = self.app
        client = app.test_client()
        # bad login
        res = client.post(app.config['BROWSERID_LOGIN_URL'], data={'assertion' : 'ducks'})
        assert res.status_code == 500
        # todo: good login

    def test_logout(self):
        app = self.app
        client = app.test_client()
        # todo: log user in, test that user is actually logged out
        # good logout
        res = client.post(app.config['BROWSERID_LOGOUT_URL'])
        assert res.status_code == 200


    def test_static_file(self):
        # todo: test that "auth.js" is compiled and 
        # available in the request contexts
        pass

    def test_multiple_applications(self):
        """
        ensures that the extension supports multiple applications.
        """
        # todo: figure out how to test no conflict 
        # between multiple applications.
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        generate_app().run()
    else:
        unittest.main()
