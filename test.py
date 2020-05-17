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
	album_sender.send(channel, url, result, rotate=rotate)

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
	print(result)
	album_sender.send(channel, url, result)

def sendPhotos(url):
	content = cached_url.get(url, force_cache=True)
	b = BeautifulSoup(content, features='lxml')
	for item in b.find_all('figure'):
		sendPhoto(url, item)
	
if __name__=='__main__':
	# test('https://www.reddit.com/r/PoliticalCompassMemes/comments/gep6km/the_political_compass_but_its_chinese_internet/')
	test('https://mp.weixin.qq.com/s?__biz=MzA4MzM2OTczMg==&amp;mid=2247502649&amp;idx=1&amp;sn=8c0ddd85a33877922dbc0c4627700704&amp;chksm=9ff50152a8828844287bd4cdc7ab87003a525f26535027087bf9feec12e57820d40775684064&amp;mpshare=1&amp;scene=1&amp;srcid=0517sQUJEOlScVlNPwI7TOgH&amp;sharer_sharetime=1589709749357&amp;sharer_shareid=ac6cbafa374000428a0e58fcfb7c4b29#rd')