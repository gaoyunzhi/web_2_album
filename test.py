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
	test('https://matters.news/@yifanfengye/%E5%A5%A5%E8%BF%90%E8%AE%B0%E5%BF%86%E7%9A%84%E5%A1%91%E9%80%A0-bafyreienav3qj2djkmi2ghw6q3konpoixrhzq7msgp2laafejz4pxmxwoq')