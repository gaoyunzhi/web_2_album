#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'web_2_album'

import cached_url
from bs4 import BeautifulSoup
import export_to_telegraph
from telegram_util import matchKey, cutCaption, getWid, parseDomain
from telegram_util import AlbumResult as Result
import readee
import time
import yaml
import sys

IMG_CLASSES = ['f-m-img', 'group-pic', 'image-wrapper', 
	'RichText', 'image-container', 'news_txt', "'article_con'", 
	'photo_wrap', 'hideBeforeLoad', 'slide_container', 'rich_media_content',
	'is-widgets', 'entry-content', 'image-show']

try:
	with open('CREDENTIALS') as f:
		credential = yaml.load(f, Loader=yaml.FullLoader)
	export_to_telegraph.token = credential.get('telegraph_token')
except:
	pass

def getCap(b, path):
	wrapper = (b.find('div', class_='weibo-text') or 
		b.find('div', class_='post f') or 
		b.find('div', class_='topic-richtext') or
		b.find('p', id='first', class_='lead'))
	if 'douban' in path:
		wrapper = b.find('blockquote') or wrapper
		title = b.find('td', class_='tablecc')
		if title:
			return title.text[3:]
	if 'zhihu' in path:
		answer = b.find('div', class_='RichContent-inner')
		answer = answer and answer.text.strip()
		if answer:
			return cutCaption(answer, '', 200)
	if not wrapper:
		return ''
	return export_to_telegraph.exportAllInText(wrapper)

def getCapForce(b, path):
	for name in ['h1', 'h2']:
		if b.find(name):
			text = b.find(name).text
			if 'douban' in path:
				return text.split('-')[-1]
			else:
				return text
	# don't know if this is the right thing to do, revisit if needed
	center = readee.export(path, content = str(b))
	try:
		return cutCaption(center.get_text(separator='\n').strip(), '', 200)
	except:
		return ''

def isWeiboArticle(path):
	return matchKey(path, ['card', 'ttarticle']) and 'weibo.c' in path

def getSrc(img, path):
	src = (img.get('data-full') or img.get('data-original') or 
		img.get('data-actualsrc') or img.get('src') or img.get('data-src'))
	src = src and src.strip()
	if not src:
		return 
	if not img.parent or not img.parent.parent:
		return 
	if 'reddit' in path:
		if img.parent.name != 'a':
			return
		return img.parent['href']
	if 'blog.boxun' in path:
		return '/'.join(path.split('/')[:-1] + [src])
	if isWeiboArticle(path) and 'sinaimg' in src:
		return src
	wrapper = img.parent.parent
	if 'detail' in sys.argv:
		print(str(wrapper.get('class')))
	if matchKey(str(wrapper.get('class')) or '', IMG_CLASSES):
		return src
	return

def enlarge(src):
	if not src:
		return None
	return src.replace('/m/', '/l/')

def withDomain(path, x):
	if x.startswith('//'):
		return 'https:' + x
	if 'slideshare' in x:
		x = x.split('?')[0]
	if x and x[0] == '/':
		return parseDomain(path) + x
	return x

def getImgs(b, path):
	raw = [enlarge(getSrc(img, path)) for img in b.find_all('img')]
	return [withDomain(path, x) for x in raw if x]

def getVideo(b):
	for video in b.find_all('video'):
		if not video.parent or not video.parent.parent:
			continue
		wrapper = video.parent.parent
		source = video.find('source')
		source = source and source['src']
		if source:
			return source
		if not matchKey(str(wrapper.get('id')), ['video_info']):
			continue
		return video['src']

def getContent(path, force_cache=False):
	if isWeiboArticle(path):
		new_url = ('https://card.weibo.com/article/m/aj/detail?id=' + 
			getWid(path) + '&_t=' + str(int(time.time())))
		json = yaml.load(
			cached_url.get(new_url, headers={'referer': path}, force_cache=force_cache), 
			Loader=yaml.FullLoader)
		return '<div><title>%s</title>%s</div>' % (json['data']['title'], json['data']['content'])
	return cached_url.get(path, force_cache=force_cache)

def get(path, force_cache=False):
	content = getContent(path, force_cache=force_cache)
	b = BeautifulSoup(content, features='lxml')
	result = Result()
	result.imgs = getImgs(b, path)
	result.cap = getCap(b, path)
	if result.imgs and not result.cap:
		# don't know if this is the right thing to do, revisit if needed
		result.cap = getCapForce(b, path)
	result.video = getVideo(b)
	result.url = path
	return result