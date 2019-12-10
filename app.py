#!/usr/bin/env python

from flask import Flask, render_template
from flask_basicauth import BasicAuth
import client
import os

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.environ['DEMO_USER']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['DEMO_PASS']

basic_auth = BasicAuth(app)


def prepare_data(secrets):
    res = []
    i = 0
    for date, message in zip(*secrets):
        date = ' {0:%d/%m/%Y a las %H:%M:%S}'.format(date)
        res.append((date, message, i))
        i += 1
    return res


@app.route('/')
@basic_auth.required
def default():
    secrets = prepare_data(client.get_secrets())
    return render_template('index.html', secrets=secrets)


@app.errorhandler(404)
def not_found(e):
    return 'Not found!', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
