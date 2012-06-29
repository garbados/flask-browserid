import unittest
import flask
from flask.ext.login import LoginManager, UserMixin
from flaskext.browserid import BrowserID
import sys
from test import test_support

class User(UserMixin):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')

USERS = (
    User(email="test@test.test", id=1),
    User(email="test2@est.test", id=2)
    )

def get_user_by_id(id):
    for user in USERS:
        if user.id == id:
            return user
    else:
        return None

def get_user(kwargs):
    for user in USERS:
        if user.email == kwargs.get('email') or user.id == kwargs.get('id'):
            return user
    else:
        return None


app = flask.Flask(__name__)

app.config['BROWSERID_LOGIN_URL'] = login_url = "/login"
app.config['BROWSERID_LOGOUT_URL'] = logout_url = "/logout"
app.config['SECRET_KEY'] = "deterministic"
app.config['TESTING'] = True

login_manager = LoginManager()
login_manager.user_loader(get_user_by_id)
login_manager.init_app(app)

browserid = BrowserID()
browserid.user_loader(get_user)
browserid.init_app(app)

@app.route('/')
def index():
    return flask.render_template('index.html')

class BasicAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.login_manager = login_manager
        self.browserid = browserid
        self.login_url = login_url
        self.logout_url = logout_url

    def test_login(self):
        # bad login
        res = self.client.post(self.login_url, data={'assertion' : 'ducks'})
        assert res.status_code == 400
        # todo: good login

    def test_logout(self):
        # good logout
        res = self.client.post(self.logout_url)
        assert res.status_code == 200

    def test_static_file(self):
        # todo: test that "auth.js" is compiled and 
        # available in the request contexts
        pass

def test_main():
    test_support.run_unittest(BasicAppTestCase)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        app.run()
    else:
        unittest.main()
