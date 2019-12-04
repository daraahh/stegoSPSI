#TODO
#lmao

import secrets
import tweepy
import argparse
import json
from PIL import Image

def authenticate():
	auth = tweepy.OAuthHandler(secrets.API_KEY,secrets.API_SECRET_KEY)
	auth.set_access_token(secrets.ACCESS_TOKEN,secrets.ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	return api

def get_imgurls(user):
	tweets = api.user_timeline(user_id=user)
	urls = []
	for status in tweets:
		for photo in status.entities['media']:
			urls.append(photo['media_url_https'])
	return urls

if __name__ == '__main__':

	api = authenticate()
	print(get_imgurls('stegospsi'))
