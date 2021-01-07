#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album
import album_sender
import yaml
from telegram.ext import Updater
import cached_url
from bs4 import BeautifulSoup
from telegram_util import AlbumResult as Result

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)
chat = tele.bot.get_chat(-1001198682178)
# chat = tele.bot.get_chat('@web_record')

def test(url, rotate=False):
	result = web_2_album.get(url)
	print(result)
	album_sender.send_v2(chat, result, rotate=rotate)

def findSrc(item):
	START_PIVOT = '"src":"'
	END_PIVOT = '","'
	for script in item.find_all('script'):
		return script.text.split(START_PIVOT)[1].split(END_PIVOT)[0]

def sendPhoto(url, item):
	result = Result()
	src = findSrc(item)
	if not src:
		return
	result.imgs = [src]
	result.cap = item.find('span', itemprop='caption').text
	album_sender.send(channel, url, result)

def sendPhotos(url):
	content = cached_url.get(url, force_cache=True)
	b = BeautifulSoup(content, features='lxml')
	for item in b.find_all('figure'):
		sendPhoto(url, item)
	
if __name__=='__main__':
	# test('https://www.douban.com/people/66855791/status/3246881937/')
	test('https://m.douban.com/people/206334353/status/3246328772')