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
channel = tele.bot.get_chat(-1001399998441)

def test(url, rotate=False):
	result = web_2_album.get(url)
	print(result)
	album_sender.send(chat, url, result, rotate=rotate)

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
	# test('https://www.reddit.com/r/PoliticalCompassMemes/comments/gep6km/the_political_compass_but_its_chinese_internet/')
	test('https://mp.weixin.qq.com/s?__biz=MzIxNDE2MjM2Mw==&mid=2652153255&idx=1&sn=c9d772a67468f724140186d115868ac4&chksm=8c4bcb73bb3c4265aea5d513c9563943ebb3506d75433972744659e2471a9adea47fabe93993&mpshare=1&scene=1&srcid=0510ryT3OFmbsvA6KI6FIIgg&sharer_sharetime=1589047401679&sharer_shareid=d0f7237f0b9b84d9bdc32b0b35eb3432#rd')