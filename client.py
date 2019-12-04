#!/usr/bin/env python

import secrets
import tweepy
import urllib.request
import tempfile as tmp
import subprocess
from dateutil import tz
import os

def authenticate():
    auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET_KEY'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    return api


def get_imginfo(api, user):
    tweets = api.user_timeline(user_id=user)
    urls = []
    dates = []
    for status in tweets:
        dates.append(status.created_at.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('Europe/Berlin')))
        for photo in status.entities['media']:
            urls.append(photo['media_url_https'])
    return urls, dates


def steghide_extract(infile, outfile, passwd):
    with subprocess.Popen([
        'steghide',
        'extract',
        '-sf', infile.name,
        '-xf', outfile.name,
        '-p', passwd,
        '-f'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        proc.wait()


def read_file(fd):
    fd.seek(0)
    return fd.read().decode('utf-8')


def get_secrets():
    api = authenticate()
    urls, dates = get_imginfo(api, 'stegospsi')
    text_secrets = []
    for url, date in zip(urls, dates):
        with tmp.NamedTemporaryFile() as t, tmp.NamedTemporaryFile() as s:
            urllib.request.urlretrieve(url, t.name)
            steghide_extract(t, s, secrets.STEG_PASS)
            text_secrets.append(read_file(s))
    return dates, text_secrets


if __name__ == '__main__':
    print('===================================================')
    for date, message in zip(*get_secrets()):
        print('[Fecha] {0:%d-%m-%Y a las %H:%M:%S}'.format(date))
        print('[+] {}'.format(message))
        print('===================================================')
