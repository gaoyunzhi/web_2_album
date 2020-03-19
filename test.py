#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album
from PIL import Image
import yaml
from telegram.ext import Updater
from telegram import InputMediaPhoto

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)

def test(url, rotate=False):
	imgs, cap = web_2_album.get(url)

	if rotate:
		for index, img_path in enumerate(imgs):
			img = Image.open(img_path)
			img = img.rotate(180)
			img.save(img_path)
			img.save('tmp_image/%s.jpg' % index)
			
	group = [InputMediaPhoto(open(imgs[0], 'rb'), caption=cap, parse_mode='Markdown')] + \
		[InputMediaPhoto(open(x, 'rb')) for x in imgs[1:]]
	if group:
		tele.bot.send_media_group(-1001198682178, group, timeout = 20*60)
	else:
		tele.bot.send_message(-1001198682178, cap, timeout = 20*60)
	
if __name__=='__main__':
	# test('http://weibointl.api.weibo.cn/share/131595305.html', rotate=True)
	test('https://twitter.com/usabignews/status/1240660005528973312')