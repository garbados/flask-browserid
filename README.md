# Flask-BrowserID

A Flask extension that provides integration with Mozilla's [BrowserID]() authentication system and Flask-Login. It exposes two routes, for login and logout, and a javascript authentication bundle that allows you to quickly create login and logout buttons.

# Installation

Install with **pip**:

    pip install git+https://github.com/garbados/flask-browserid.git

# Quickstart

Flask-BrowserID requires that Flask-Login's LoginManager be configured and registered with the app first, like so:

    from flask import Flask
    from flask.ext.login import LoginManager
    from flask.ext.browserid import BrowserID
    from my_stuff import get_user_by_id # finds a user by their id
    from other_stuff import get_user # finds a user based on BrowserID response

    app = Flask(__name__)
    
    login_manager = LoginManager()
    login_manager.user_loader(get_user_by_id)
    login_manager.init_app(app)

    browser_id = BrowserID()
    browser_id.user_loader(get_user)
    browser_id.init_app(app)

Now the routes `/api/login` and `/api/logout` have been registered with your app. A javascript bundle, `auth_script`, has also been added to the top level of your request context, so you can access it in templates like so:

[Note: `auth_script` requires JQuery and Mozilla's `include.js`]

    <html>
        <head>
            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
            <script src="https://login.persona.org/include.js" type="text/javascript"></script>
            <script type="text/javascript">{{ auth_script|safe }}</script>
        </head>
        <body>
            {% if current_user.is_authenticated() %}
                <button id="browserid-logout">Logout</button>
            {% else %}        
                <button id="browserid-login">Login</button>
            {% endif %}
        </body>
    </html>

Thanks to `auth_script`, clicking the `Login` button on that page will attempt to log you in using BrowserID. If you're already logged in, then clicking `Logout` will log you out.

# Required Configuration

Flask-BrowserID requires a function that takes the data returned by BrowserID and uses it to find and return a user, which Flask-BrowserID then logs in using Flask-Login. If the function can't find a user, it can attempt to create a user using the data given. If a user could neither be found nor created, the function should return None. The data returned by BrowserID will look something like this if successful:

    {
        "status": "okay",
        "email": "lloyd@example.com",
        "audience": "https://mysite.com",
        "expires": 1308859352261,
        "issuer": "browserid.org"
    }

Or this, if not:

    {
        "status": "failure",
        "reason": "no certificate provided"
    }

BrowserID's response will have already been parsed from JSON into a dict by the time it reaches your `user_loader` function.

# Optional Configuration

You can set the URLs Flask-BrowserID uses for login and logout by setting the following in your application's configuration:

* `BROWSERID_LOGIN_URL`: defaults to `/api/login`
* `BROWSERID_LOGOUT_URL`: defaults to `/api/logout`

See [Flask Configuration Handling](http://flask.pocoo.org/docs/config/) for more on how to configure your application.

# Testing

Running `python setup.py test` will run the extension's automated test suite, but some tests can only be run (presently) by manually starting up the server and clicking around. To do so, from the extension's root directory, run `python tests/__init__.py -i`. The `-i` flag tells the test suite to skip normal testing and instead run the testing application with a test template so you can click around.

# Credits

Many thanks to [Flask-Mongoengine](https://github.com/MongoEngine/flask-mongoengine), who I based the structure of this extension on, and to [Flask-Login](https://flask-login.readthedocs.org/en/latest/), for generally being a pretty sweet extension.
