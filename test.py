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
	print(result)
	album_sender.send(chat, url, result, rotate=rotate)
	
if __name__=='__main__':
	test('https://www.douban.com/group/topic/174521906/?dt_platform=com.douban.activity.wechat_friends&dt_dapp=1')