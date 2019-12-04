#!/usr/bin/env python3

import secrets
import tweepy
import argparse
from PIL import Image
import subprocess
import tempfile as tmp


def authenticate():
    auth = tweepy.OAuthHandler(secrets.API_KEY, secrets.API_SECRET_KEY)
    auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def tweet_image(img):
    response = api.media_upload(img)
    status = api.update_status(media_ids=[response.media_id])
    return status


def hide(img, text):
    stego_img = Image.open(img)

    # stego

    return stego_img


def destroy_tweets(api, tweets):
    if tweets:
        for t in tweets:
            api.destroy_status(t.id)
        return True
    else:
        return False


def steghide_embed(infile_name, text, passwd):
    with tmp.NamedTemporaryFile() as t:
        t.write(text.encode('utf-8'))
        t.seek(0)
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
        # TODO
        img = hide(args.img, args.text)
        img.save(args.output)

    elif args.img:
        # Tweet
        api = authenticate()
        steghide_embed(args.img, args.text, secrets.STEG_PASS)
        tweet_image(args.img)

    elif args.purge:
        api = authenticate()
        tweets = api.user_timeline()
        res = destroy_tweets(api, tweets)
        if res:
            print('All tweets have been destroyed')
        else:
            print('No tweets')
