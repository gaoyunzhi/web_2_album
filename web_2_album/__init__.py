#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'web_2_album'

import cached_url
from bs4 import BeautifulSoup
import export_to_telegraph
from telegram_util import matchKey, cutCaption
from telegram_util import AlbumResult as Result

IMG_CLASSES = ['f-m-img', 'group-pic', 'image-wrapper', 'RichText']

try:
	with open('CREDENTIALS') as f:
		credential = yaml.load(f, Loader=yaml.FullLoader)
	export_to_telegraph.token = credential.get('telegraph_token')
except:
	pass

def getCap(b):
	wrapper = b.find('div', class_='weibo-text') or \
		b.find('div', class_='post f') or b.find('div', class_='topic-richtext')
	if 'douban' in str(b):
		wrapper = b.find('blockquote') or wrapper
	if 'zhihu' in str(b):
		answer = b.find('div', class_='RichContent-inner')
		answer = answer and answer.text.strip()
		if answer:
			return cutCaption(answer, '', 200)
	if not wrapper:
		return ''
	return export_to_telegraph.exportAllInText(wrapper)

def getSrc(img):
	src = img.get('data-original') or img.get('data-actualsrc') or \
		(img.get('src') and img.get('src').strip())
	if not src:
		return 
	if not img.parent or not img.parent.parent:
		return 
	wrapper = img.parent.parent
	if matchKey(str(wrapper.get('class')) or '', IMG_CLASSES):
		return src
	return

def getImgs(b):
	raw = [getSrc(img) for img in b.find_all('img')]
	return [x for x in raw if x]

def getVideo(b):
	for video in b.find_all('video'):
		if not video.parent or not video.parent.parent:
			continue
		wrapper = video.parent.parent
		if not matchKey(str(wrapper.get('id')), ['video_info']):
			continue
		return video['src']

def get(path, force_cache=False):
	content = cached_url.get(path, force_cache=force_cache)
	b = BeautifulSoup(content, features='lxml')
	result = Result()
	result.imgs = getImgs(b)
	result.cap = getCap(b)
	result.video = getVideo(b)
	return result