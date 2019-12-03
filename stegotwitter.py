#!/usr/bin/env python3

import secrets
import tweepy
import argparse
from PIL import Image

def authenticate():
	auth = tweepy.OAuthHandler(secrets.API_KEY,secrets.API_SECRET_KEY)
	auth.set_access_token(secrets.ACCESS_TOKEN,secrets.ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	return api

# Habrá que cambiarlo con la implementación de la parte de stego
# Probablemente reemplazar api.media_upload(img) por api.media_upload(filename,file)
# siendo file un objeto File, aunque no lo he probado aun
def tweet_image(img):
	response = api.media_upload(img)
	status = api.update_status(media_ids=[response.media_id])
	return status

def hide(img,text):
	stego_img = Image.open(img)

	#stego

	return stego_img


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--image',dest='img',help='image to tweet')
	parser.add_argument('-t','--text', type=str, dest='text',help='text to hide')
	parser.add_argument('-o','--output',dest='output', help='output file name')
	args = parser.parse_args()

	if args.img and args.output and args.text:
		# Crear stego image en local
		img = hide(args.img,args.text)
		img.save(args.output)
	elif args.img:
		# Tweet
		api = authenticate()
		tweet_image(args.img)
