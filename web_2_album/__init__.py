#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'web_2_album'

import math
import os
import cached_url
from bs4 import BeautifulSoup
from telegram_util import cutCaption
import pic_cut
import readee
import export_to_telegraph

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

def getQuote(b):
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

def getAuthor(b):
	candidates = [
		lambda x: x.find('header').find('div', class_='m-text-box').find('a'),
		lambda x: x.find('a', class_='lnk-people'),
	]
	author = getCandidate(candidates, b, '原文')
	return author.text.strip()	

def getCap(b, path, cap_limit):
	quote = getQuote(b)
	if not quote:
		return ''
	author = getAuthor(b)
	suffix = ' [%s](%s)' % (author, path)
	return cutCaption(quote, suffix, cap_limit)

def getSrc(img):
	src = img.get('src') and img.get('src').strip()
	if not src:
		return 
	if 'width: 100%;' in str(img.attrs):
		return src
	if img.get('class') and 'upload-pic' in img.get('class'):
		return src
	return

def compare(c1, c2):
	# assume c1 does not have image, otherwise, we will return 
	if c2[0]:
		return c2
	if len(c1[1]) > len(c2[1]):
		return c1
	return c2

def getImages(b, image_limit):
	raw = [getSrc(img) for img in b.find_all('img')]
	raw = [x for x in raw if x]
	return pic_cut.getCutImages(raw, image_limit)

def get(path, cap_limit = 1000, text_limit = 4000, 
		img_limit = 9, ok_no_image = False):
	content = cached_url.get(path)
	b1 = readee.export(path, content=content)
	b2 = BeautifulSoup(content, features="html.parser")
	candidate = [], ''
	for b in [b1, b2]:
		img = getImages(b, img_limit)
		cap = getCap(b2, path, cap_limit = cap_limit if img else text_limit)
		if img:
			return img, cap
		candidate = compare(candidate, (img, cap))
	return candidate