#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'web_2_album'

import cached_url
from bs4 import BeautifulSoup
import pic_cut
import readee
import export_to_telegraph
from telegram_util import matchKey

class Result(object):
	def __init__(self):
		self.imgs = []
		self.cap = ''
		self.video = ''

try:
	with open('CREDENTIALS') as f:
		credential = yaml.load(f, Loader=yaml.FullLoader)
	export_to_telegraph.token = credential.get('telegraph_token')
except:
	pass

def getCap(b):
	wrapper = b.find('div', class_='weibo-text') or b.find('blockquote')
	if not wrapper:
		return ''
	return export_to_telegraph.exportAllInText(wrapper)

def getSrc(img):
	src = img.get('src') and img.get('src').strip()
	if not src:
		return 
	if not img.parent or not img.parent.parent:
		return 
	wrapper = img.parent.parent
	if matchKey(str(wrapper.get('class')) or '', ['f-m-img', 'group-pic']):
		return src
	return

def getImgs(b, img_limit):
	raw = [getSrc(img) for img in b.find_all('img')]
	raw = [x for x in raw if x]
	return pic_cut.getCutImages(raw, img_limit)

def getVideo(b):
	for video in b.find_all('video'):
		if not video.parent or not video.parent.parent:
			continue
		wrapper = video.parent.parent
		if not matchKey(str(wrapper.get('id')), ['video_info']):
			continue
		return video['src']

def get(path, img_limit = 9):
	content = cached_url.get(path)
	b = readee.export(path, content=content)
	result = Result()
	result.imgs = getImgs(b, img_limit)
	result.cap = getCap(b)
	result.video = getVideo(b)
	return result