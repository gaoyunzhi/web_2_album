#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album
import album_sender
import yaml
from telegram.ext import Updater
import cached_url
from bs4 import BeautifulSoup

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)
chat = tele.bot.get_chat(-1001198682178)
channel = tele.bot.get_chat(-1001399998441)

def test(url, rotate=False):
	result = web_2_album.get(url)
	# print(result)
	album_sender.send(chat, url, result, rotate=rotate)

def sendPhoto(item):
	print(str(item))

def sendPhotos(url):
	content = cached_url.get(url, force_cache=True)
	b = BeautifulSoup(content, features='lxml')
	for item in b.find_all('img'):
		sendPhoto(item)
		return # test
	
if __name__=='__main__':
	# test('https://www.reddit.com/r/PoliticalCompassMemes/comments/gep6km/the_political_compass_but_its_chinese_internet/')
	sendPhotos('https://www.nationalgeographic.com/photography/best-pictures-2019/')