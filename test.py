#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import web_2_album
import album_sender
import yaml
from telegram.ext import Updater

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)
chat = tele.bot.get_chat(-1001198682178)

def test(url, rotate=False):
	result = web_2_album.get(url)
	album_sender.send(chat, url, result, rotate=rotate)
	
if __name__=='__main__':
	test('https://www.douban.com/group/topic/169845329/')
	# test('https://www.douban.com/people/ayongli/status/2832255859/')
	# test('http://jandan.net/2020/03/30/gamer-girls.html')
	# test('http://weibointl.api.weibo.cn/share/131595305.html', rotate=True)
	# test('http://www.douban.com/people/RonaldoLuiz/status/2877273534/')
	# test('https://weibointl.api.weibo.cn/share/133847669.html?weibo_id=4468334634971089&from=groupmessage&isappinstalled=0')