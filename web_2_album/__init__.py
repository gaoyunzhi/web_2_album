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
	quote = candidate.text.strip()
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
	author = getAuthor(b)
	suffix = ' [%s](%s)' % (author, path)
	return cutCaption(quote, suffix, cap_limit)

def getImages(b, image_limit):
	raw = []
	for img in b.find_all('img'):
		if img.get('src') and 'width: 100%;' in str(img.attrs):
			raw.append(img.get('src'))
	return pic_cut.getCutImages(raw, image_limit)

def get(path, cap_limit = 1000, img_limit = 9):
	content = cached_url.get(path)
	b1 = readee.export(path, content=content)
	b2 = BeautifulSoup(content, features="html.parser")
	for b in [b1, b2]:
		img, cap = getImages(b, img_limit), getCap(b2, path, cap_limit = cap_limit)
		if img:
			return img, cap



	

