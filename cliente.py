#!/usr/bin/env python

import secrets
import tweepy
import urllib.request
import tempfile as tmp
import subprocess


def authenticate():
    auth = tweepy.OAuthHandler(secrets.API_KEY, secrets.API_SECRET_KEY)
    auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def get_imginfo(user):
    tweets = api.user_timeline(user_id=user)
    urls = []
    dates = []
    for status in tweets:
        dates.append(status.created_at)
        for photo in status.entities['media']:
            urls.append(photo['media_url_https'])
    return urls,dates


def steghide_extract(infile, outfile, passwd):
    with subprocess.Popen([
        'steghide',
        'extract',
        '-sf', t.name,
        '-xf', s.name,
        '-p', secrets.STEG_PASS,
        '-f'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        proc.wait()


def read_file(fd):
    if fd.read() != b'':
        fd.seek(0)
        message = fd.read().decode('utf-8')
        print('[+] {}'.format(message))
    print('===================================================')

if __name__ == '__main__':
    api = authenticate()
    urls,dates = get_imginfo('stegospsi')
    print('===================================================')
    for url,date in zip(urls,dates):
        print('[Fecha] {0:%d-%m-%Y a las %H:%M:%S}'.format(date))
        with tmp.NamedTemporaryFile() as t, tmp.NamedTemporaryFile() as s:
            urllib.request.urlretrieve(url, t.name)
            steghide_extract(t.name, s.name, secrets.STEG_PASS)
            read_file(s)
