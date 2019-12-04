#!/usr/bin/env python3

import tweepy
import argparse
from PIL import Image
import subprocess
import tempfile as tmp
import os

def authenticate():
    auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET_KEY'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    return api


def tweet_image(img):
    response = api.media_upload(img)
    status = api.update_status(media_ids=[response.media_id])
    return status

def destroy_tweets(api, tweets):
    if tweets:
        for t in tweets:
            api.destroy_status(t.id)
        return True
    else:
        return False


def steghide_embed(infile_name, text, passwd, outfile_name):

    with tmp.NamedTemporaryFile() as t:
        t.write(text.encode('utf-8'))
        t.seek(0)
        if outfile_name:
            with subprocess.Popen([
                'steghide',
                'embed',
                '-cf', infile_name,
                '-ef', t.name,
                '-sf', outfile_name,
                '-p', passwd,
                '-f'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                proc.wait()
        else:
            with subprocess.Popen([
                'steghide',
                'embed',
                '-cf', infile_name,
                '-ef', t.name,
                '-p', passwd,
                '-f'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                proc.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', dest='img', help='image to tweet')
    parser.add_argument('-t', '--text', type=str, dest='text',
                        help='text to hide')
    parser.add_argument('-o', '--output', dest='output',
                        help='output file name')
    parser.add_argument('-p', '--purge', action='store_true',
                        help='destroy all tweets')
    args = parser.parse_args()

    if args.img and args.output and args.text:
        # Crear stego image en local
        steghide_embed(args.img, args.text, os.environ['STEG_PASS'],args.output)
    elif args.img:
        # Tweet
        api = authenticate()
        steghide_embed(args.img, args.text, os.environ['STEG_PASS'],None)
        tweet_image(args.img)

    elif args.purge:
        api = authenticate()
        tweets = api.user_timeline()
        res = destroy_tweets(api, tweets)
        if res:
            print('All tweets have been destroyed')
        else:
            print('No tweets')
