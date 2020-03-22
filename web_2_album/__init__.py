#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'web_2_album'

import cached_url
from bs4 import BeautifulSoup
import pic_cut
import readee
import export_to_telegraph

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

def clearUrl(url):
	if 'weibo' in url:
		index = url.find('?')
		if index > -1:
			url = url[:index]
	if url.endswith('/'):
		url = url[:-1]
	if '_' in url:
		url = '[网页链接](%s)' % url
	url = url.replace('https://', '')
	url = url.replace('http://', '')
	return url

def getCandidate(candidates, input, default):
	for c in candidates:
		try:
			result = c(input)
			if result:
				return result
		except:
			pass
	return default

def getCap(b):
	candidates = [
		lambda x: x.find('div', class_='weibo-text'), 
		lambda x: x.find('blockquote'),
	]
	candidate = getCandidate(candidates, b, '')
	if not candidate:
		return ''
	quote = BeautifulSoup(str(candidate).replace('<br/>', '\n'), features='lxml')\
		.text.strip()
	for link in candidate.find_all('a', title=True, href=True):
		url = link['title']
		url = clearUrl(export_to_telegraph.export(url) or url)
		quote = quote.replace(link['href'], ' ' + url + ' ')
	return quote

def getSrc(img):
	src = img.get('src') and img.get('src').strip()
	if not src:
		return 
	if 'width: 100%;' in str(img.attrs):
		return src
	if img.get('class') and 'upload-pic' in img.get('class'):
		return src
	return

def getImgs(b, img_limit):
	raw = [getSrc(img) for img in b.find_all('img')]
	raw = [x for x in raw if x]
	return pic_cut.getCutImages(raw, img_limit)

def get(path, img_limit = 9):
	content = cached_url.get(path)
	b = readee.export(path, content=content)
	# b2 = BeautifulSoup(content, features="html.parser")
	result = Result()
	result.imgs = getImgs(b, img_limit)
	result.cap = getCap(b)
	return result