"""
Flask-MongoEngine
--------------

Flask support for BrowserID authentication, using flask-login

Links
`````

* `Mozilla BrowserID documentation
  <https://developer.mozilla.org/en/BrowserID>`

"""
from setuptools import setup


setup(
    name='Flask-BrowserID',
    version='0.0.1',
    url='https://github.com/garbados/flask-browserid',
    license='MIT',
    author='Max Thayer',
    author_email='garbados@gmail.com',
    description='Flask support for BrowserID authentication',
    long_description=file.read(open('README.md', 'r')),
    packages=['flaskext',
              'flaskext.browserid',
              ],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'flask-login',
        'requests',
    ],
    include_package_data=True,
    tests_require=[
        'Attest',
    ],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='tests.flask_browserid',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
