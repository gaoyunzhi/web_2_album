#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'web_2_album'

import math
import os
import cached_url
from bs4 import BeautifulSoup
from telegram_util import cutCaption
import pic_cut

def getCap(b, path, cap_limit):
	quote = b.find('div', class_='weibo-text').text.strip()
	author = b.find('header').find('div', class_='m-text-box').text.strip()
	suffix = '[%s](%s)' % (author, path)
	return cutCaption(quote, suffix, cap_limit)

def getImages(b, image_limit):
	raw = []
	for img in b.find_all('img'):
		if img.get('src') and 'width: 100%;' in str(img.attrs):
			raw.append(img.get('src'))
	return pic_cut.getCutImages(raw, image_limit)

def get(path, cap_limit = 1000, img_limit = 9):
	b = BeautifulSoup(cached_url.get(path), features="html.parser")
	return getImages(b, img_limit), getCap(b, path, cap_limit = cap_limit)



	

