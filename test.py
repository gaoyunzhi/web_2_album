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
	test('https://mp.weixin.qq.com/s?__biz=MjM5NTUxOTc4Mw==&amp;mid=2650489538&amp;idx=1&amp;sn=ed052626f2e1a5719ae742cdd866c0cb&amp;chksm=bef8ae8a898f279c09fbb6b1d3feda84eb73e3470831c713656fa37da935beaf4790706af796&amp;mpshare=1&amp;scene=1&amp;srcid=0428zXHtLxyYwGalv3ZcEchf&amp;sharer_sharetime=1588052927935&amp;sharer_shareid=e6f2072629a326da73cf7d26fd42a655#rd')