#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album
from PIL import Image
import yaml
from telegram.ext import Updater
from telegram import InputMediaPhoto, InputMediaVideo
import cached_url
import pic_cut
from telegram_util import cutCaption

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)

def test(url, rotate=False):
	result = web_2_album.get(url)
	suffix = '[source](%s)' % url

	if result.video:
		with open('tmp/video.mp4', 'wb') as f:
			f.write(cached_url.get(result.video, force_cache=True, mode='b'))
		group = [InputMediaVideo(open('tmp/video.mp4', 'rb'), 
			caption=cutCaption(result.cap, suffix, 1000), parse_mode='Markdown')]
		return tele.bot.send_media_group(-1001198682178, group, timeout = 20*60)
		

	imgs = pic_cut.getCutImages(result.imgs, 9)	
	if imgs:
		imgs = pic_cut.getCutImages(result.imgs, 9)
		if rotate:
			for img_path in imgs:
				img = Image.open(img_path)
				img = img.rotate(180)
				img.save(img_path)
		group = [InputMediaPhoto(open(imgs[0], 'rb'), 
			caption=cutCaption(result.cap, suffix, 1000), parse_mode='Markdown')] + \
			[InputMediaPhoto(open(x, 'rb')) for x in imgs[1:]]
		return tele.bot.send_media_group(-1001198682178, group, timeout = 20*60)

	tele.bot.send_message(-1001198682178, cutCaption(result.cap, suffix, 4000), 
		timeout = 20*60)
	
if __name__=='__main__':
	test('http://weibointl.api.weibo.cn/share/131595305.html', rotate=True)
	test('http://www.douban.com/people/RonaldoLuiz/status/2877273534/')
	# test('https://weibointl.api.weibo.cn/share/133847669.html?weibo_id=4468334634971089&from=groupmessage&isappinstalled=0')